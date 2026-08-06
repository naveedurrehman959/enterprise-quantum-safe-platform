# backend/app/migration_engine/services.py

from datetime import datetime
from app.audit.services import create_audit_log
from app.extensions import db
from app.risk_assessment.services import RiskAssessmentService
from app.policy_engine.services import PolicyEngineService

from app.crypto.algorithm_registry import (
    get_algorithm_details
)


class MigrationEngineService:


    @staticmethod
    def analyze_migration(data):

        algorithm = data.get("algorithm")

        asset_name = data.get(
            "asset_name",
            "unknown_asset"
        )


        if not algorithm:

            return {
                "error": "algorithm is required"
            }


        algorithm = algorithm.upper()


        # Get algorithm intelligence from registry

        algorithm_details = get_algorithm_details(
            algorithm
        )


        # Risk Assessment

        risk_result = RiskAssessmentService.assess_algorithm(
            algorithm
        )


        # Policy Evaluation

        policy_result = PolicyEngineService.check_algorithm(
            algorithm
        )


        risk_level = risk_result.get(
            "risk_level",
            algorithm_details.get(
                "risk_level",
                "UNKNOWN"
            )
        )


        policy_status = policy_result.get(
            "status",
            "UNKNOWN"
        )


        recommended_algorithm = algorithm_details.get(
            "replacement",
            []
        )


        migration_strategy = algorithm_details.get(
            "migration_strategy",
            "MANUAL_REVIEW"
        )


        # ---------------------------------
        # Critical / High Risk Migration
        # ---------------------------------

        if risk_level in [
            "CRITICAL",
            "HIGH"
        ]:


            return {

                "asset_name":
                    asset_name,


                "current_algorithm":
                    algorithm,


                "algorithm_category":
                    algorithm_details.get(
                        "category"
                    ),


                "risk_level":
                    risk_level,


                "risk_score":
                    risk_result.get(
                        "risk_score"
                    ),


                "policy_status":
                    policy_status,


                "migration_required":
                    True,


                "migration_strategy":
                    migration_strategy,


                "recommended_algorithm":
                    recommended_algorithm,


                "migration_phase":
                    "PHASE_1",


                "recommendation":
                    "Replace vulnerable algorithm with PQC hybrid deployment",


                "timestamp":
                    datetime.utcnow().isoformat()

            }



        # ---------------------------------
        # Conditional Migration
        # ---------------------------------

        if policy_status == "CONDITIONAL":


            return {

                "asset_name":
                    asset_name,


                "current_algorithm":
                    algorithm,


                "algorithm_category":
                    algorithm_details.get(
                        "category"
                    ),


                "risk_level":
                    risk_level,


                "policy_status":
                    policy_status,


                "migration_required":
                    True,


                "migration_strategy":
                    "HYBRID_MODE",


                "recommended_algorithm":
                    recommended_algorithm,


                "migration_phase":
                    "PHASE_2",


                "recommendation":
                    "Deploy classical and PQC algorithms together",


                "timestamp":
                    datetime.utcnow().isoformat()

            }



        # ---------------------------------
        # Quantum Safe Algorithm
        # ---------------------------------

        return {

            "asset_name":
                asset_name,


            "current_algorithm":
                algorithm,


            "algorithm_category":
                algorithm_details.get(
                    "category"
                ),


            "risk_level":
                risk_level,


            "policy_status":
                policy_status,


            "migration_required":
                False,


            "migration_strategy":
                "NO_MIGRATION_REQUIRED",


            "recommended_algorithm":
                algorithm,


            "migration_phase":
                "COMPLETED",


            "recommendation":
                "Algorithm is quantum-safe",


            "timestamp":
                datetime.utcnow().isoformat()

        }



    @staticmethod
    def generate_plan(algorithm):


        details = get_algorithm_details(
            algorithm.upper()
        )


        return {


            "source_algorithm":
                algorithm,


            "algorithm_category":
                details.get(
                    "category"
                ),


            "target_algorithm":
                details.get(
                    "replacement"
                ),


            "migration_steps":[

                "Discover cryptographic asset",

                "Classify cryptographic algorithm",

                "Perform quantum risk assessment",

                "Validate security policy",

                "Generate PQC keys",

                "Enable hybrid cryptography",

                "Deploy PQC certificates",

                "Retire legacy algorithm"

            ],


            "status":
                "READY_FOR_MIGRATION",


            "created_at":
                datetime.utcnow().isoformat()

        }



    @staticmethod
    def migration_report():


        return {


            "module":
                "Migration Engine",


            "status":
                "ACTIVE",


            "supported_algorithms":[

                "RSA",

                "ECC",

                "ECDSA",

                "ECDHE",

                "AES",

                "ML-KEM",

                "ML-DSA"

            ],


            "features":[

                "Algorithm Classification",

                "Quantum Risk Detection",

                "PQC Recommendation",

                "Hybrid Migration Planning"

            ],


            "compliance":[

                "NIST PQC",

                "ISO 27001",

                "PCI DSS"

            ],


            "generated_at":
                datetime.utcnow().isoformat()

        }
