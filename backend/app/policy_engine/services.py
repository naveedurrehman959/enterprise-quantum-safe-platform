from datetime import datetime

from app.extensions import db

from app.algorithm_inventory.models import AlgorithmAsset
from app.algorithm_inventory.services import AlgorithmInventoryService

from app.risk_assessment.services import RiskAssessmentService

from app.audit.services import create_audit_log


class PolicyEngineService:
    """
    Enterprise Quantum-Safe Policy Engine

    Responsibilities
    ----------------
    • Policy Enforcement
    • Algorithm Approval
    • Risk-Based Decisions
    • Asset Discovery Integration
    • Dashboard Summary
    """

    # ==========================================================
    # Enterprise Policy
    # ==========================================================

    @staticmethod
    def get_policy():

        algorithms = AlgorithmAsset.query.order_by(
            AlgorithmAsset.algorithm_name
        ).all()

        return {

            "policy_name":
                "Enterprise Quantum-Safe Policy",

            "security_level":
                "HIGH",

            "deployment_mode":
                algorithms[0].deployment_mode
                if algorithms
                else "CLASSICAL",

            "approved_algorithms": [

                a.algorithm_name

                for a in algorithms

                if a.allowed

            ],

            "blocked_algorithms": [

                a.algorithm_name

                for a in algorithms

                if not a.allowed

            ],

            "active_algorithms": [

                a.algorithm_name

                for a in algorithms

                if a.active

            ],

            "total_algorithms":
                len(algorithms),

            "allowed_count":
                sum(a.allowed for a in algorithms),

            "blocked_count":
                sum(not a.allowed for a in algorithms),

            "active_count":
                sum(a.active for a in algorithms),

            "timestamp":
                datetime.utcnow().isoformat()

        }

    # ==========================================================
    # Policy Evaluation
    # ==========================================================

    @staticmethod
    def evaluate_policy(algorithm_name):
        """
        Enterprise policy evaluation.
        """

        algorithm_name = algorithm_name.upper().strip()

        algorithm = AlgorithmInventoryService.get_algorithm_by_name(
            algorithm_name
        )

        if algorithm is None:

            AlgorithmInventoryService.auto_register_algorithm(
                algorithm_name
            )

            algorithm = AlgorithmInventoryService.get_algorithm_by_name(
                algorithm_name
            )

        risk = RiskAssessmentService.assess_algorithm(
            algorithm_name
        )

        if risk["risk_level"] == "CRITICAL":

            decision = "BLOCK"

        elif risk["risk_level"] == "HIGH":

            decision = "MIGRATION_REQUIRED"

        elif risk["risk_level"] == "MEDIUM":

            decision = "HYBRID_REQUIRED"

        elif risk["risk_level"] == "SAFE":

            decision = "ALLOW"

        else:

            decision = "MANUAL_REVIEW"

        return {

            "algorithm":
                algorithm_name,

            "decision":
                decision,

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
    # Existing API (Compatible)
    # ==========================================================

    @staticmethod
    def check_algorithm(algorithm_name):
        """
        Existing endpoint compatibility.
        """

        policy = PolicyEngineService.evaluate_policy(
            algorithm_name
        )

        algorithm = AlgorithmInventoryService.get_algorithm_by_name(
            algorithm_name
        )

        if algorithm is None:

            return {

                "status": "UNKNOWN",

                "decision": "MANUAL_REVIEW"

            }

        if policy["decision"] == "BLOCK":

            create_audit_log(

                user_id=None,

                action="POLICY_BLOCK",

                module="POLICY_ENGINE",

                status="FAILED",

                description=(
                    f"{algorithm.algorithm_name} "
                    f"blocked by enterprise policy."
                )

            )

            db.session.commit()

            return {

                "algorithm":
                    algorithm.algorithm_name,

                "status":
                    "BLOCKED",

                "decision":
                    "REJECT",

                "risk_level":
                    policy["risk_level"],

                "recommended_algorithm":
                    policy["recommended_algorithm"]

            }

        if algorithm.active:

            return {

                "algorithm":
                    algorithm.algorithm_name,

                "status":
                    "ACTIVE",

                "decision":
                    "ALLOW",

                "deployment_mode":
                    algorithm.deployment_mode,

                "risk_level":
                    policy["risk_level"]

            }

        return {

            "algorithm":
                algorithm.algorithm_name,

            "status":
                "INACTIVE",

            "decision":
                "NOT_SELECTED",

            "recommended_mode":
                algorithm.recommended_mode,

            "recommended_algorithm":
                policy["recommended_algorithm"]

        }

    # ==========================================================
    # Asset Discovery Integration
    # ==========================================================

    @staticmethod
    def check_discovered_asset(asset):
        """
        Evaluate a discovered asset.
        """

        policy = PolicyEngineService.evaluate_policy(
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
                policy["decision"],

            "risk_level":
                policy["risk_level"],

            "recommendation":
                policy["recommended_algorithm"]

        }

    # ==========================================================
    # Dashboard Summary
    # ==========================================================

    @staticmethod
    def dashboard_summary():

        algorithms = AlgorithmAsset.query.all()

        assessment = RiskAssessmentService.assess_inventory()

        return {

            "total_algorithms":
                len(algorithms),

            "approved":
                assessment["approved"],

            "blocked":
                assessment["blocked"],

            "migration_required":
                assessment["migration_required"],

            "critical":
                assessment["critical_risk"],

            "high":
                assessment["high_risk"],

            "safe":
                assessment["safe_assets"],

            "timestamp":
                datetime.utcnow().isoformat()

        }
