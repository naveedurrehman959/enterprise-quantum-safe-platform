# backend/app/risk_assessment/services.py

from app.algorithm_inventory.models import AlgorithmAsset


class RiskAssessmentService:


    RISK_DATABASE = {


        # =========================
        # Asymmetric Cryptography
        # =========================

        "RSA-1024": {
            "category": "ASYMMETRIC_ENCRYPTION",
            "risk_level": "CRITICAL",
            "risk_score": 100,
            "quantum_vulnerable": True,
            "recommendation": "Replace with ML-KEM-768",
            "recommended_algorithm": "ML-KEM-768",
        },


        "RSA-2048": {
            "category": "ASYMMETRIC_ENCRYPTION",
            "risk_level": "HIGH",
            "risk_score": 85,
            "quantum_vulnerable": True,
            "recommendation": "Deploy Hybrid ECDHE + ML-KEM",
            "recommended_algorithm": "ECDHE + ML-KEM-768",
        },


        "RSA-4096": {
            "category": "ASYMMETRIC_ENCRYPTION",
            "risk_level": "HIGH",
            "risk_score": 75,
            "quantum_vulnerable": True,
            "recommendation": "Plan PQC migration",
            "recommended_algorithm": "ML-KEM-768",
        },


        "ECDSA": {
            "category": "DIGITAL_SIGNATURE",
            "risk_level": "HIGH",
            "risk_score": 90,
            "quantum_vulnerable": True,
            "recommendation": "Replace with ML-DSA",
            "recommended_algorithm": "ML-DSA-65",
        },


        "ECDHE": {
            "category": "KEY_EXCHANGE",
            "risk_level": "HIGH",
            "risk_score": 80,
            "quantum_vulnerable": True,
            "recommendation": "Enable Hybrid TLS",
            "recommended_algorithm": "ECDHE + ML-KEM-768",
        },


        # =========================
        # Symmetric Crypto
        # =========================


        "AES-128": {
            "category": "SYMMETRIC_ENCRYPTION",
            "risk_level": "MEDIUM",
            "risk_score": 50,
            "quantum_vulnerable": True,
            "recommendation": "Upgrade AES strength",
            "recommended_algorithm": "AES-256-GCM",
        },


        "AES-256-GCM": {
            "category": "SYMMETRIC_ENCRYPTION",
            "risk_level": "SAFE",
            "risk_score": 5,
            "quantum_vulnerable": False,
            "recommendation": "Approved",
            "recommended_algorithm": "AES-256-GCM",
        },


        # =========================
        # Hashing
        # =========================


        "SHA1": {
            "category": "HASH",
            "risk_level": "CRITICAL",
            "risk_score": 95,
            "quantum_vulnerable": True,
            "recommendation": "Replace with SHA3-512",
            "recommended_algorithm": "SHA3-512",
        },


        "SHA-256": {
            "category": "HASH",
            "risk_level": "SAFE",
            "risk_score": 10,
            "quantum_vulnerable": False,
            "recommendation": "Approved",
            "recommended_algorithm": "SHA-256",
        },


        "SHA3-512": {
            "category": "HASH",
            "risk_level": "SAFE",
            "risk_score": 5,
            "quantum_vulnerable": False,
            "recommendation": "Quantum resistant",
            "recommended_algorithm": "SHA3-512",
        },


        # =========================
        # Post Quantum Algorithms
        # =========================


        "ML-KEM": {
            "category": "PQC_KEM",
            "risk_level": "SAFE",
            "risk_score": 0,
            "quantum_vulnerable": False,
            "recommendation": "Approved PQC KEM",
            "recommended_algorithm": "ML-KEM",
        },


        "ML-KEM-768": {
            "category": "PQC_KEM",
            "risk_level": "SAFE",
            "risk_score": 0,
            "quantum_vulnerable": False,
            "recommendation": "Recommended",
            "recommended_algorithm": "ML-KEM-768",
        },


        "ML-DSA": {
            "category": "PQC_SIGNATURE",
            "risk_level": "SAFE",
            "risk_score": 0,
            "quantum_vulnerable": False,
            "recommendation": "Approved PQC Signature",
            "recommended_algorithm": "ML-DSA",
        },


        "ML-DSA-65": {
            "category": "PQC_SIGNATURE",
            "risk_level": "SAFE",
            "risk_score": 0,
            "quantum_vulnerable": False,
            "recommendation": "Recommended",
            "recommended_algorithm": "ML-DSA-65",
        },


    }



    @staticmethod
    def get_status():

        return {

            "engine": "ACTIVE",
            "quantum_threat_detection": "ENABLED",
            "risk_database": "LOADED"

        }



    @classmethod
    def assess_algorithm(cls, algorithm):

        algorithm = algorithm.upper()


        for key,value in cls.RISK_DATABASE.items():

            if key in algorithm:


                migration_required = (
                    value["risk_level"]
                    != "SAFE"
                )


                if value["risk_level"] == "CRITICAL":

                    decision="BLOCKED"


                elif migration_required:

                    decision="MIGRATION_REQUIRED"


                else:

                    decision="APPROVED"



                return {

                    "algorithm":algorithm,
                    **value,
                    "migration_required":
                        migration_required,
                    "decision":
                        decision

                }



        return {

            "algorithm":algorithm,
            "category":"UNKNOWN",
            "risk_level":"UNKNOWN",
            "risk_score":50,
            "quantum_vulnerable":True,
            "migration_required":True,
            "decision":"MANUAL_REVIEW",
            "recommendation":
                "Manual assessment required"

        }



    @classmethod
    def assess_inventory(cls):

        assets = AlgorithmAsset.query.all()


        result={

            "total_assets":len(assets),
            "critical_risk":0,
            "high_risk":0,
            "medium_risk":0,
            "safe_assets":0

        }


        for asset in assets:


            risk = cls.assess_algorithm(
                asset.algorithm_name
            )


            level=risk["risk_level"]


            if level=="CRITICAL":
                result["critical_risk"]+=1


            elif level=="HIGH":
                result["high_risk"]+=1


            elif level=="MEDIUM":
                result["medium_risk"]+=1


            elif level=="SAFE":
                result["safe_assets"]+=1



        return result



    @classmethod
    def inventory(cls):

        vulnerable=[]

        safe=[]


        for algo,data in cls.RISK_DATABASE.items():


            if data["quantum_vulnerable"]:

                vulnerable.append(algo)

            else:

                safe.append(algo)



        return {

            "vulnerable_algorithms":vulnerable,

            "quantum_safe_algorithms":safe

        }
