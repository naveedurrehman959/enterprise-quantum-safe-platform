ALGORITHM_DATABASE = {

    "RSA-1024": {
        "quantum_vulnerable": True,
        "risk_level": "CRITICAL",
        "risk_score": 100,
        "recommendation": "ML-KEM-768",
        "migration_required": True
    },


    "RSA-2048": {
        "quantum_vulnerable": True,
        "risk_level": "HIGH",
        "risk_score": 80,
        "recommendation": "Hybrid ML-KEM-768",
        "migration_required": True
    },


    "ECDSA": {
        "quantum_vulnerable": True,
        "risk_level": "HIGH",
        "risk_score": 85,
        "recommendation": "ML-DSA-65",
        "migration_required": True
    },


    "ECDHE": {
        "quantum_vulnerable": True,
        "risk_level": "MEDIUM",
        "risk_score": 50,
        "recommendation": "ECDHE + ML-KEM-768",
        "migration_required": True
    },


    "SHA1": {
        "quantum_vulnerable": True,
        "risk_level": "CRITICAL",
        "risk_score": 100,
        "recommendation": "SHA3-512",
        "migration_required": True
    },


    "DES": {
        "quantum_vulnerable": True,
        "risk_level": "CRITICAL",
        "risk_score": 100,
        "recommendation": "AES-256-GCM",
        "migration_required": True
    },


    "AES-256": {
        "quantum_vulnerable": False,
        "risk_level": "SAFE",
        "risk_score": 0,
        "recommendation": "KEEP",
        "migration_required": False
    },


    "ML-KEM-768": {
        "quantum_vulnerable": False,
        "risk_level": "SAFE",
        "risk_score": 0,
        "recommendation": "KEEP",
        "migration_required": False
    },


    "ML-DSA-65": {
        "quantum_vulnerable": False,
        "risk_level": "SAFE",
        "risk_score": 0,
        "recommendation": "KEEP",
        "migration_required": False
    }

}
class RiskAssessmentService:


    @staticmethod
    def assess_algorithm(algorithm):

        result = ALGORITHM_DATABASE.get(
            algorithm
        )


        if not result:

            return {

                "algorithm": algorithm,

                "risk_level":"UNKNOWN",

                "risk_score":50,

                "quantum_vulnerable":True,

                "recommendation":
                "Manual Review",

                "migration_required":True

            }


        return {

            "algorithm":algorithm,

            **result

        }
