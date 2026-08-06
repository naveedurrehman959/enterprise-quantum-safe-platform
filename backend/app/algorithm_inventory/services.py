from datetime import datetime

from app import db
from .models import AlgorithmAsset


class AlgorithmInventoryService:

    @staticmethod
    def analyze_algorithm(name):

        algorithm = name.upper()

        result = {
            "category": "UNKNOWN",
            "risk_level": "UNKNOWN",
            "recommended_mode": "HYBRID",
            "allowed": True,
            "active": False,
            "description": "",
        }

        # ---------- Classical ----------

        if algorithm.startswith("RSA"):

            result.update({
                "category": "CLASSICAL",
                "risk_level": "HIGH",
                "recommended_mode": "HYBRID",
                "description": "Classical RSA algorithm vulnerable to future quantum attacks."
            })

        elif algorithm.startswith("ECC") or algorithm.startswith("ECDSA"):

            result.update({
                "category": "CLASSICAL",
                "risk_level": "HIGH",
                "recommended_mode": "HYBRID",
                "description": "Elliptic Curve Cryptography."
            })

        # ---------- Symmetric ----------

        elif algorithm.startswith("AES"):

            result.update({
                "category": "SYMMETRIC",
                "risk_level": "SAFE",
                "recommended_mode": "ALL",
                "active": True,
                "description": "Quantum-resistant symmetric encryption."
            })

        elif algorithm.startswith("CHACHA20"):

            result.update({
                "category": "SYMMETRIC",
                "risk_level": "SAFE",
                "recommended_mode": "ALL",
                "active": True,
                "description": "Modern symmetric cipher."
            })

        # ---------- Hash ----------

        elif algorithm.startswith("SHA"):

            result.update({
                "category": "HASH",
                "risk_level": "SAFE",
                "recommended_mode": "ALL",
                "active": True,
                "description": "Cryptographic hash algorithm."
            })

        # ---------- PQC ----------

        elif algorithm.startswith("ML-KEM"):

            result.update({
                "category": "PQC_KEM",
                "risk_level": "SAFE",
                "recommended_mode": "PURE_PQC",
                "description": "NIST standardized post-quantum key encapsulation."
            })

        elif algorithm.startswith("ML-DSA"):

            result.update({
                "category": "PQC_SIGNATURE",
                "risk_level": "SAFE",
                "recommended_mode": "PURE_PQC",
                "description": "NIST standardized post-quantum digital signature."
            })

        elif algorithm.startswith("SLH-DSA"):

            result.update({
                "category": "PQC_SIGNATURE",
                "risk_level": "SAFE",
                "recommended_mode": "PURE_PQC",
                "description": "Stateless hash-based digital signature."
            })

        # ---------- Hybrid ----------

        elif "+" in algorithm:

            result.update({
                "category": "HYBRID",
                "risk_level": "SAFE",
                "recommended_mode": "HYBRID",
                "description": "Hybrid cryptography combining classical and post-quantum algorithms."
            })

        return result

    @staticmethod
    def list_algorithms():

        return [
            algorithm.to_dict()
            for algorithm in AlgorithmAsset.query.order_by(
                AlgorithmAsset.category,
                AlgorithmAsset.algorithm_name
            ).all()
        ]

    @staticmethod
    def create_algorithm(data):

        analysis = AlgorithmInventoryService.analyze_algorithm(
            data["algorithm_name"]
        )

        algorithm = AlgorithmAsset(

            algorithm_name=data["algorithm_name"],

            category=analysis["category"],

            version=data.get("version"),

            key_size=data.get("key_size"),

            allowed=analysis["allowed"],

            active=analysis["active"],

            deployment_mode="CLASSICAL",

            risk_level=analysis["risk_level"],

            recommended_mode=analysis["recommended_mode"],

            description=analysis["description"]

        )

        db.session.add(algorithm)
        db.session.commit()

        return algorithm.to_dict()

    @staticmethod
    def set_allowed(algorithm_id, allowed):

        algorithm = AlgorithmAsset.query.get_or_404(
            algorithm_id
        )

        algorithm.allowed = allowed

        db.session.commit()

        return algorithm.to_dict()

    @staticmethod
    def set_active(algorithm_id, active):

        algorithm = AlgorithmAsset.query.get_or_404(
            algorithm_id
        )

        algorithm.active = active

        db.session.commit()

        return algorithm.to_dict()

    @staticmethod
    def set_deployment_mode(mode):

        mode = mode.upper()

        algorithms = AlgorithmAsset.query.all()

        for algorithm in algorithms:

            if mode == "CLASSICAL":

                algorithm.active = (
                    algorithm.allowed and
                    algorithm.category in [
                        "CLASSICAL",
                        "SYMMETRIC",
                        "HASH"
                    ]
                )

            elif mode == "HYBRID":

                algorithm.active = (
                    algorithm.allowed and
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
                    algorithm.allowed and
                    algorithm.category in [
                        "PQC_KEM",
                        "PQC_SIGNATURE",
                        "SYMMETRIC",
                        "HASH"
                    ]
                )

            algorithm.deployment_mode = mode

        db.session.commit()

        return {
            "message": "Deployment mode updated successfully.",
            "deployment_mode": mode
        }

    @staticmethod
    def get_summary():

        algorithms = AlgorithmAsset.query.all()

        return {

            "module": "Algorithm Inventory",

            "total_algorithms":
                len(algorithms),

            "allowed_algorithms":
                sum(a.allowed for a in algorithms),

            "disabled_algorithms":
                sum(not a.allowed for a in algorithms),

            "active_algorithms":
                sum(a.active for a in algorithms),

            "classical":
                sum(a.category == "CLASSICAL"
                    for a in algorithms),

            "pqc":
                sum(a.category.startswith("PQC")
                    for a in algorithms),

            "hybrid":
                sum(a.category == "HYBRID"
                    for a in algorithms),

            "deployment_mode":
                algorithms[0].deployment_mode
                if algorithms else "CLASSICAL",

            "timestamp":
                datetime.utcnow().isoformat()

        }
