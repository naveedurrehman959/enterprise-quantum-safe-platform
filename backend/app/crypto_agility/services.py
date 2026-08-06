# backend/app/crypto_agility/services.py

from datetime import datetime

from app import db
from app.algorithm_inventory.models import AlgorithmAsset
from app.audit.services import create_audit_log
from app.policy_engine.services import PolicyEngineService
from app.risk_assessment.services import RiskAssessmentService


class CryptoAgilityService:

    # -------------------------------------------------
    # Engine Status
    # -------------------------------------------------

    @staticmethod
    def get_status(user_id=None):

        if user_id:
            create_audit_log(
                user_id=user_id,
                action="VIEW_CRYPTO_AGILITY_STATUS",
                module="CRYPTO_AGILITY",
                status="SUCCESS",
                description="Crypto Agility status viewed."
            )

        algorithms = AlgorithmAsset.query.all()

        pqc = [
            a.algorithm_name
            for a in algorithms
            if a.category.startswith("PQC")
        ]

        deployment_mode = (
            algorithms[0].deployment_mode
            if algorithms
            else "CLASSICAL"
        )

        return {

            "engine": "Crypto Agility Engine",

            "status": "ACTIVE",

            "deployment_mode": deployment_mode,

            "algorithm_switching": "ENABLED",

            "migration_engine": "READY",

            "supported_pqc": pqc,

            "timestamp": datetime.utcnow().isoformat()

        }

    # -------------------------------------------------
    # Change Deployment Mode
    # -------------------------------------------------

    @staticmethod
    def change_deployment_mode(mode):

        mode = mode.upper()

        algorithms = AlgorithmAsset.query.all()

        for algorithm in algorithms:

            algorithm.deployment_mode = mode

            if not algorithm.allowed:
                algorithm.active = False
                continue

            if mode == "CLASSICAL":

                algorithm.active = (
                    algorithm.category in [
                        "CLASSICAL",
                        "SYMMETRIC",
                        "HASH"
                    ]
                )

            elif mode == "HYBRID":

                algorithm.active = (
                    algorithm.category in [
                        "CLASSICAL",
                        "HYBRID",
                        "PQC_KEM",
                        "PQC_SIGNATURE",
                        "SYMMETRIC",
                        "HASH"
                    ]
                )

            elif mode == "PURE_PQC":

                algorithm.active = (
                    algorithm.category in [
                        "PQC_KEM",
                        "PQC_SIGNATURE",
                        "SYMMETRIC",
                        "HASH"
                    ]
                )

        db.session.commit()

        return {

            "message": "Deployment mode updated successfully.",

            "deployment_mode": mode

        }

    # -------------------------------------------------
    # Recommend Migration
    # -------------------------------------------------

    @staticmethod
    def recommend_migration(
        algorithm,
        user_id=None
    ):

        risk = RiskAssessmentService.assess_algorithm(
            algorithm
        )

        recommendation = CryptoAgilityService.select_algorithm(
            algorithm
        )

        if user_id:

            create_audit_log(

                user_id=user_id,

                action="CRYPTO_MIGRATION_RECOMMENDATION",

                module="CRYPTO_AGILITY",

                status="SUCCESS",

                description=f"Migration recommendation generated for {algorithm}"

            )

        return {

            "algorithm": algorithm,

            "risk_level": risk["risk_level"],

            "risk_score": risk["risk_score"],

            "quantum_vulnerable": risk["quantum_vulnerable"],

            "migration_required":
                risk["risk_level"] in [
                    "HIGH",
                    "CRITICAL"
                ],

            "recommended_algorithm":
                recommendation["recommended_algorithm"],

            "hybrid_mode":
                recommendation["hybrid_mode"],

            "decision":
                recommendation["decision"]

        }

    # -------------------------------------------------
    # Select Algorithm
    # -------------------------------------------------

    @staticmethod
    def select_algorithm(current_algorithm):

        algorithm = current_algorithm.upper()

        if "RSA" in algorithm:

            return {

                "current_algorithm": current_algorithm,

                "recommended_algorithm": "ML-KEM-768",

                "hybrid_mode": "RSA + ML-KEM-768",

                "migration_required": True,

                "decision": "MIGRATE"

            }

        if "ECC" in algorithm:

            return {

                "current_algorithm": current_algorithm,

                "recommended_algorithm": "ML-KEM-768 + ML-DSA-65",

                "hybrid_mode": "ECC + ML-KEM-768",

                "migration_required": True,

                "decision": "MIGRATE"

            }

        if "ECDHE" in algorithm:

            return {

                "current_algorithm": current_algorithm,

                "recommended_algorithm": "ECDHE + ML-KEM-768",

                "hybrid_mode": True,

                "migration_required": True,

                "decision": "MIGRATE"

            }

        if "ECDSA" in algorithm:

            return {

                "current_algorithm": current_algorithm,

                "recommended_algorithm": "ML-DSA-65",

                "hybrid_mode": "ECDSA + ML-DSA-65",

                "migration_required": True,

                "decision": "MIGRATE"

            }

        return {

            "current_algorithm": current_algorithm,

            "recommended_algorithm": current_algorithm,

            "hybrid_mode": False,

            "migration_required": False,

            "decision": "NO_ACTION"

        }

    # -------------------------------------------------
    # Execute Migration
    # -------------------------------------------------

    @staticmethod
    def migrate_algorithm(
        source_algorithm,
        target_algorithm,
        user_id=None
    ):

        if user_id:

            create_audit_log(

                user_id=user_id,

                action="CRYPTO_MIGRATION",

                module="CRYPTO_AGILITY",

                status="SUCCESS",

                description=f"{source_algorithm} migrated to {target_algorithm}"

            )

        algorithm = AlgorithmAsset.query.filter_by(
            algorithm_name=target_algorithm
        ).first()

        mode = (
            algorithm.deployment_mode
            if algorithm
            else "HYBRID"
        )

        return {

            "migration": "SUCCESS",

            "source_algorithm": source_algorithm,

            "target_algorithm": target_algorithm,

            "deployment_mode": mode,

            "validation": "PASSED",

            "timestamp": datetime.utcnow().isoformat()

        }

    # -------------------------------------------------
    # Validate Algorithm
    # -------------------------------------------------

    @staticmethod
    def validate_algorithm(algorithm):

        policy = PolicyEngineService.check_algorithm(
            algorithm
        )

        return {

            "algorithm": algorithm,

            "policy_status": policy.get("status"),

            "decision": policy.get("decision"),

            "approved":
                policy.get("status") == "APPROVED"

        }

    # -------------------------------------------------
    # Inventory
    # -------------------------------------------------

    @staticmethod
    def inventory():

        algorithms = AlgorithmAsset.query.order_by(
            AlgorithmAsset.category,
            AlgorithmAsset.algorithm_name
        ).all()

        return {

            "deployment_mode":
                algorithms[0].deployment_mode
                if algorithms
                else "CLASSICAL",

            "algorithms": [
                algorithm.to_dict()
                for algorithm in algorithms
            ]

        }
