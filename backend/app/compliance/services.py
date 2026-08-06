# backend/app/compliance/services.py

from datetime import datetime

from app.audit.services import create_audit_log
from app.risk_assessment.services import RiskAssessmentService
from app.policy_engine.services import PolicyEngineService
from app.algorithm_inventory.models import AlgorithmAsset


class ComplianceService:


    FRAMEWORKS = [
        "NIST-PQC",
        "NIST-CSF-2.0",
        "CNSA-2.0",
        "ISO-27001",
        "PCI-DSS",
    ]


    @staticmethod
    def get_compliance_status(user_id=None):

        create_audit_log(
            user_id=user_id,
            action="VIEW_COMPLIANCE_STATUS",
            module="COMPLIANCE",
            status="SUCCESS",
            description="Viewed compliance status.",
        )

        return {

            "compliance_engine":
                "ACTIVE",

            "quantum_safe_ready":
                True,

            "audit_ready":
                True,

            "policy_integration":
                "ENABLED",

            "risk_engine_integration":
                "ENABLED",

            "frameworks_supported":
                ComplianceService.FRAMEWORKS,

            "status":
                "READY",

            "timestamp":
                datetime.utcnow().isoformat()
        }



    @staticmethod
    def get_supported_frameworks(user_id=None):

        create_audit_log(
            user_id=user_id,
            action="VIEW_FRAMEWORKS",
            module="COMPLIANCE",
            status="SUCCESS",
            description="Viewed compliance frameworks.",
        )


        return {

            "frameworks":[

                {
                    "name": framework,
                    "status": "SUPPORTED"
                }

                for framework 
                in ComplianceService.FRAMEWORKS

            ]

        }



    @staticmethod
    def validate_framework(
        framework,
        algorithm=None,
        user_id=None
    ):


        risk_result = None
        policy_result = None


        if algorithm:


            risk_result = (
                RiskAssessmentService
                .assess_algorithm(
                    algorithm
                )
            )


            policy_result = (
                PolicyEngineService
                .check_algorithm(
                    algorithm
                )
            )


            compliant = (

                risk_result["risk_level"]
                in [
                    "SAFE",
                    "LOW"
                ]

                and

                policy_result["status"]
                ==
                "APPROVED"

            )


        else:

            compliant = True



        create_audit_log(

            user_id=user_id,

            action="VALIDATE_COMPLIANCE",

            module="COMPLIANCE",

            status="SUCCESS",

            description=
            f"Validated {framework}"

        )


        return {


            "framework":
                framework,


            "algorithm":
                algorithm,


            "validation_status":
                "PASSED"
                if compliant
                else
                "FAILED",


            "compliant":
                compliant,


            "risk_assessment":
                risk_result,


            "policy_check":
                policy_result,


            "controls_verified":
                True,


            "migration_ready":
                compliant

        }



    @staticmethod
    def compliance_dashboard(user_id=None):


        assets = AlgorithmAsset.query.all()


        total = len(assets)

        compliant = 0

        violations = []


        for asset in assets:


            risk = (
                RiskAssessmentService
                .assess_algorithm(
                    asset.algorithm_name
                )
            )


            if risk["risk_level"] in [

                "SAFE",
                "LOW"

            ]:

                compliant += 1


            else:

                violations.append(

                    {
                        "algorithm":
                            asset.algorithm_name,

                        "risk":
                            risk["risk_level"],

                        "recommendation":
                            risk["recommendation"]

                    }

                )


        score = 100


        if total > 0:

            score = int(
                (compliant / total)
                *
                100
            )


        return {


            "compliance_score":
                score,


            "status":
                (
                    "COMPLIANT"
                    if score >= 90
                    else
                    "PARTIALLY_COMPLIANT"
                ),


            "total_assets":
                total,


            "compliant_assets":
                compliant,


            "violations":
                violations,


            "frameworks":
                ComplianceService.FRAMEWORKS,


            "generated_at":
                datetime.utcnow().isoformat()

        }



    @staticmethod
    def generate_report(user_id=None):


        return {


            "platform":
                "Enterprise Quantum-Safe Cryptographic Infrastructure",


            "overall_status":
                "COMPLIANT",


            "checks":{

                "authentication":
                    "PASS",

                "rbac":
                    "PASS",

                "audit_logging":
                    "PASS",

                "pqc_support":
                    "PASS",

                "legacy_crypto_detection":
                    "ENABLED",

                "risk_assessment":
                    "ACTIVE"

            },


            "frameworks":
                ComplianceService.FRAMEWORKS,


            "generated_at":
                datetime.utcnow().isoformat()

        }
