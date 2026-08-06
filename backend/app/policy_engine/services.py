from app.algorithm_inventory.models import AlgorithmAsset
from app.audit.services import create_audit_log
from app.extensions import db


class PolicyEngineService:

    @staticmethod
    def get_policy():

        algorithms = AlgorithmAsset.query.order_by(
            AlgorithmAsset.algorithm_name
        ).all()

        return {

            "policy_name": "Enterprise Quantum-Safe Policy",

            "security_level": "HIGH",

            "deployment_mode":
                algorithms[0].deployment_mode
                if algorithms else "CLASSICAL",

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
                sum(not a.allowed for a in algorithms)

        }

    @staticmethod
    def check_algorithm(algorithm):

        algorithm = AlgorithmAsset.query.filter_by(
            algorithm_name=algorithm
        ).first()

        if not algorithm:

            return {

                "status": "UNKNOWN",

                "decision": "REJECT",

                "message": "Algorithm not found in inventory."

            }

        if not algorithm.allowed:

            create_audit_log(

                user_id=None,

                action="POLICY_BLOCK",

                module="POLICY_ENGINE",

                status="FAILED",

                description=f"{algorithm.algorithm_name} is disabled"

            )

            db.session.commit()

            return {

                "algorithm":
                    algorithm.algorithm_name,

                "status":
                    "BLOCKED",

                "decision":
                    "REJECT"

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
                    algorithm.deployment_mode

            }

        return {

            "algorithm":
                algorithm.algorithm_name,

            "status":
                "INACTIVE",

            "decision":
                "NOT_SELECTED",

            "recommended_mode":
                algorithm.recommended_mode

        }
