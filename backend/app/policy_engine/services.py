from datetime import datetime

from app.extensions import db

from app.algorithm_inventory.models import AlgorithmAsset
from app.algorithm_inventory.services import AlgorithmInventoryService
from app.risk_assessment.services import RiskAssessmentService

from .models import CryptoPolicy


class PolicyEngineService:
    """
    Enterprise Quantum-Safe Policy Engine.

    Responsibilities
    ----------------
    - Flexible cryptographic policy configuration
    - Classical / Hybrid / PQC policy modes
    - Algorithm allow/block enforcement
    - Risk-aware decisions
    - Asset discovery integration
    - Dashboard summary
    """

    # ==========================================================
    # DEFAULT POLICY
    # ==========================================================

    DEFAULT_POLICIES = {

        # Classical algorithms
        "RSA-1024": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 10
        },

        "RSA-2048": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 20
        },

        "RSA-4096": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 30
        },

        "ECDSA": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 30
        },

        "ECC": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 30
        },

        "ECDHE": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 30
        },

        # Hybrid
        "ECDHE + ML-KEM-768": {
            "enabled": True,
            "deployment_mode": "HYBRID",
            "enforcement_action": "ALLOW",
            "priority": 1
        },

        # PQC
        "ML-KEM-768": {
            "enabled": True,
            "deployment_mode": "PURE_PQC",
            "enforcement_action": "ALLOW",
            "priority": 1
        },

        "ML-DSA-65": {
            "enabled": True,
            "deployment_mode": "PURE_PQC",
            "enforcement_action": "ALLOW",
            "priority": 1
        },

        "AES-256-GCM": {
            "enabled": True,
            "deployment_mode": "PURE_PQC",
            "enforcement_action": "ALLOW",
            "priority": 1
        },

        # Weak algorithms
        "SHA1": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 5
        },

        "DES": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 5
        },

        "3DES": {
            "enabled": False,
            "deployment_mode": "CLASSICAL",
            "enforcement_action": "BLOCK",
            "priority": 5
        }
    }

    # ==========================================================
    # INITIALIZE DEFAULT POLICY
    # ==========================================================

    @staticmethod
    def initialize_default_policy():

        for algorithm_name, config in (
            PolicyEngineService.DEFAULT_POLICIES.items()
        ):

            policy = CryptoPolicy.query.filter_by(
                algorithm_name=algorithm_name
            ).first()

            if policy:
                continue

            policy = CryptoPolicy(
                algorithm_name=algorithm_name,
                enabled=config["enabled"],
                deployment_mode=config["deployment_mode"],
                enforcement_action=config["enforcement_action"],
                priority=config["priority"]
            )

            db.session.add(policy)

        db.session.commit()

    # ==========================================================
    # GET POLICY
    # ==========================================================

    @staticmethod
    def get_policy():

        PolicyEngineService.initialize_default_policy()

        policies = CryptoPolicy.query.order_by(
            CryptoPolicy.priority.asc(),
            CryptoPolicy.algorithm_name.asc()
        ).all()

        approved = []
        blocked = []
        conditional = []

        for policy in policies:

            if (
                policy.enabled
                and policy.enforcement_action == "ALLOW"
            ):
                approved.append(
                    policy.algorithm_name
                )

            elif policy.enforcement_action == "BLOCK":
                blocked.append(
                    policy.algorithm_name
                )

            else:
                conditional.append(
                    policy.algorithm_name
                )

        deployment_modes = {
            "CLASSICAL": [],
            "HYBRID": [],
            "PURE_PQC": []
        }

        for policy in policies:

            deployment_modes.setdefault(
                policy.deployment_mode,
                []
            ).append(
                policy.algorithm_name
            )

        return {

            "policy_name":
                "Enterprise Quantum-Safe Policy",

            "security_level":
                "HIGH",

            "status":
                "ACTIVE",

            "policy_status":
                "ACTIVE",

            "approved_algorithms":
                approved,

            "allowed_algorithms":
                approved,

            "blocked_algorithms":
                blocked,

            "conditional_algorithms":
                conditional,

            "deployment_modes":
                deployment_modes,

            "total_algorithms":
                len(policies),

            "allowed_count":
                len(approved),

            "blocked_count":
                len(blocked),

            "conditional_count":
                len(conditional),

            "policies": [
                policy.to_dict()
                for policy in policies
            ],

            "timestamp":
                datetime.utcnow().isoformat()
        }

    # ==========================================================
    # LIST POLICIES
    # ==========================================================

    @staticmethod
    def list_policies():

        PolicyEngineService.initialize_default_policy()

        policies = CryptoPolicy.query.order_by(
            CryptoPolicy.priority.asc(),
            CryptoPolicy.algorithm_name.asc()
        ).all()

        return [
            policy.to_dict()
            for policy in policies
        ]

    # ==========================================================
    # UPDATE POLICY
    # ==========================================================

    @staticmethod
    def update_policy(
        algorithm_name,
        enabled=None,
        deployment_mode=None,
        enforcement_action=None
    ):

        algorithm_name = algorithm_name.strip()

        policy = CryptoPolicy.query.filter_by(
            algorithm_name=algorithm_name
        ).first()

        if policy is None:

            policy = CryptoPolicy(
                algorithm_name=algorithm_name
            )

            db.session.add(policy)

        if enabled is not None:
            policy.enabled = bool(enabled)

        if deployment_mode:

            deployment_mode = deployment_mode.upper()

            allowed_modes = [
                "CLASSICAL",
                "HYBRID",
                "PURE_PQC"
            ]

            if deployment_mode not in allowed_modes:
                raise ValueError(
                    "Invalid deployment mode. "
                    "Use CLASSICAL, HYBRID or PURE_PQC."
                )

            policy.deployment_mode = deployment_mode

        if enforcement_action:

            enforcement_action = (
                enforcement_action.upper()
            )

            allowed_actions = [
                "ALLOW",
                "BLOCK",
                "MIGRATE",
                "REVIEW"
            ]

            if enforcement_action not in allowed_actions:
                raise ValueError(
                    "Invalid enforcement action."
                )

            policy.enforcement_action = (
                enforcement_action
            )

        policy.updated_at = datetime.utcnow()

        db.session.commit()

        return policy.to_dict()

    # ==========================================================
    # EVALUATE POLICY
    # ==========================================================

    @staticmethod
    def evaluate_policy(algorithm_name):

        algorithm_name = (
            algorithm_name.strip()
        )

        PolicyEngineService.initialize_default_policy()

        policy = CryptoPolicy.query.filter_by(
            algorithm_name=algorithm_name
        ).first()

        risk = RiskAssessmentService.assess_algorithm(
            algorithm_name
        )

        # ------------------------------------------------------
        # Explicit policy always has priority
        # ------------------------------------------------------

        if policy:

            if policy.enforcement_action == "BLOCK":

                decision = "BLOCK"

            elif policy.enforcement_action == "MIGRATE":

                decision = "MIGRATION_REQUIRED"

            elif policy.enforcement_action == "REVIEW":

                decision = "MANUAL_REVIEW"

            elif (
                policy.enabled
                and policy.enforcement_action == "ALLOW"
            ):

                decision = "ALLOW"

            else:

                decision = "BLOCK"

            return {

                "algorithm":
                    algorithm_name,

                "decision":
                    decision,

                "policy_enabled":
                    policy.enabled,

                "deployment_mode":
                    policy.deployment_mode,

                "enforcement_action":
                    policy.enforcement_action,

                "risk_level":
                    risk["risk_level"],

                "risk_score":
                    risk["risk_score"],

                "quantum_vulnerable":
                    risk.get(
                        "quantum_vulnerable"
                    ),

                "recommended_algorithm":
                    risk.get(
                        "recommended_algorithm"
                    ),

                "recommendation":
                    risk.get(
                        "recommendation"
                    )
            }

        # ------------------------------------------------------
        # Unknown algorithm
        # ------------------------------------------------------

        return {

            "algorithm":
                algorithm_name,

            "decision":
                "MANUAL_REVIEW",

            "policy_enabled":
                False,

            "deployment_mode":
                "UNKNOWN",

            "enforcement_action":
                "REVIEW",

            "risk_level":
                risk["risk_level"],

            "risk_score":
                risk["risk_score"],

            "recommended_algorithm":
                risk.get(
                    "recommended_algorithm"
                ),

            "recommendation":
                risk.get(
                    "recommendation"
                )
        }

    # ==========================================================
    # CHECK ALGORITHM
    # ==========================================================

    @staticmethod
    def check_algorithm(algorithm_name):

        result = PolicyEngineService.evaluate_policy(
            algorithm_name
        )

        if result["decision"] == "BLOCK":

            return {
                **result,
                "status": "BLOCKED"
            }

        if result["decision"] == "ALLOW":

            return {
                **result,
                "status": "ACTIVE"
            }

        if result["decision"] == "MIGRATION_REQUIRED":

            return {
                **result,
                "status": "MIGRATION_REQUIRED"
            }

        return {
            **result,
            "status": "REVIEW_REQUIRED"
        }

    # ==========================================================
    # DISCOVERED ASSET
    # ==========================================================

    @staticmethod
    def check_discovered_asset(asset):

        result = PolicyEngineService.evaluate_policy(
            asset.public_key_algorithm
        )

        return {

            "hostname":
                asset.hostname,

            "ip_address":
                asset.ip_address,

            "algorithm":
                asset.public_key_algorithm,

            "decision":
                result["decision"],

            "risk_level":
                result["risk_level"],

            "risk_score":
                result["risk_score"],

            "deployment_mode":
                result.get(
                    "deployment_mode"
                ),

            "recommendation":
                result.get(
                    "recommended_algorithm"
                )
        }

    # ==========================================================
    # DASHBOARD SUMMARY
    # ==========================================================

    @staticmethod
    def dashboard_summary():

        policy = PolicyEngineService.get_policy()

        return {

            "total_algorithms":
                policy["total_algorithms"],

            "approved":
                policy["allowed_count"],

            "blocked":
                policy["blocked_count"],

            "conditional":
                policy["conditional_count"],

            "approved_algorithms":
                policy["approved_algorithms"],

            "blocked_algorithms":
                policy["blocked_algorithms"],

            "timestamp":
                datetime.utcnow().isoformat()
        }
