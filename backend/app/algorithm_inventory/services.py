
from datetime import datetime

from app import db
from .models import AlgorithmAsset


class AlgorithmInventoryService:
    """
    Enterprise Algorithm Inventory Service

    Responsibilities:
    - Analyze algorithms
    - Create algorithms
    - Prevent duplicates
    - Auto-register discovered algorithms
    - Deployment mode management
    """

    # ==========================================================
    # ANALYZE ALGORITHM
    # ==========================================================

    @staticmethod
    def analyze_algorithm(name):

        algorithm = name.upper().strip()

        result = {
            "category": "UNKNOWN",
            "risk_level": "UNKNOWN",
            "recommended_mode": "HYBRID",
            "allowed": True,
            "active": False,
            "description": "",
        }

        # ======================================================
        # Classical Algorithms
        # ======================================================

        if algorithm.startswith("RSA"):

            result.update({
                "category": "CLASSICAL",
                "risk_level": "HIGH",
                "recommended_mode": "HYBRID",
                "description": (
                    "Classical RSA algorithm vulnerable "
                    "to future quantum attacks."
                ),
            })

        elif (
            algorithm.startswith("ECC")
            or algorithm.startswith("ECDSA")
            or algorithm.startswith("ECDHE")
        ):

            result.update({
                "category": "CLASSICAL",
                "risk_level": "HIGH",
                "recommended_mode": "HYBRID",
                "description": (
                    "Elliptic Curve Cryptography is "
                    "vulnerable to future quantum attacks."
                ),
            })

        # ======================================================
        # Symmetric Algorithms
        # ======================================================

        elif algorithm.startswith("AES"):

            result.update({
                "category": "SYMMETRIC",
                "risk_level": "SAFE",
                "recommended_mode": "PURE_PQC",
                "active": True,
                "description": (
                    "Modern symmetric encryption. "
                    "AES-256 is recommended for quantum-safe use."
                ),
            })

        elif algorithm.startswith("CHACHA20"):

            result.update({
                "category": "SYMMETRIC",
                "risk_level": "SAFE",
                "recommended_mode": "PURE_PQC",
                "active": True,
                "description": (
                    "Modern symmetric cipher with "
                    "strong security properties."
                ),
            })

        # ======================================================
        # Hash Algorithms
        # ======================================================

        elif algorithm.startswith("SHA"):

            if algorithm in ["SHA1", "SHA-1"]:

                result.update({
                    "category": "HASH",
                    "risk_level": "CRITICAL",
                    "recommended_mode": "HYBRID",
                    "allowed": False,
                    "active": False,
                    "description": (
                        "SHA-1 is deprecated and must not "
                        "be used for secure cryptographic operations."
                    ),
                })

            else:

                result.update({
                    "category": "HASH",
                    "risk_level": "SAFE",
                    "recommended_mode": "PURE_PQC",
                    "active": True,
                    "description": (
                        "Modern cryptographic hash algorithm."
                    ),
                })

        # ======================================================
        # Post-Quantum KEM
        # ======================================================

        elif algorithm.startswith("ML-KEM"):

            result.update({
                "category": "PQC_KEM",
                "risk_level": "SAFE",
                "recommended_mode": "PURE_PQC",
                "active": True,
                "description": (
                    "NIST standardized post-quantum "
                    "key encapsulation mechanism."
                ),
            })

        # ======================================================
        # Post-Quantum Signatures
        # ======================================================

        elif algorithm.startswith("ML-DSA"):

            result.update({
                "category": "PQC_SIGNATURE",
                "risk_level": "SAFE",
                "recommended_mode": "PURE_PQC",
                "active": True,
                "description": (
                    "NIST standardized post-quantum "
                    "digital signature algorithm."
                ),
            })

        elif algorithm.startswith("SLH-DSA"):

            result.update({
                "category": "PQC_SIGNATURE",
                "risk_level": "SAFE",
                "recommended_mode": "PURE_PQC",
                "active": True,
                "description": (
                    "Stateless hash-based post-quantum "
                    "digital signature algorithm."
                ),
            })

        # ======================================================
        # Weak Algorithms
        # ======================================================

        elif algorithm in ["DES", "3DES", "TRIPLEDES"]:

            result.update({
                "category": "CLASSICAL",
                "risk_level": "CRITICAL",
                "recommended_mode": "HYBRID",
                "allowed": False,
                "active": False,
                "description": (
                    "Deprecated symmetric encryption algorithm "
                    "that must not be used."
                ),
            })

        # ======================================================
        # Hybrid Algorithms
        # ======================================================

        elif "+" in algorithm:

            result.update({
                "category": "HYBRID",
                "risk_level": "SAFE",
                "recommended_mode": "HYBRID",
                "active": True,
                "description": (
                    "Hybrid cryptography combining classical "
                    "and post-quantum algorithms."
                ),
            })

        return result

    # ==========================================================
    # LIST ALGORITHMS
    # ==========================================================

    @staticmethod
    def list_algorithms():

        return [
            algorithm.to_dict()
            for algorithm in AlgorithmAsset.query.order_by(
                AlgorithmAsset.category,
                AlgorithmAsset.algorithm_name
            ).all()
        ]

    # ==========================================================
    # CREATE ALGORITHM
    # ==========================================================

    @staticmethod
    def create_algorithm(data):
        """
        Create a new algorithm if it does not already exist.

        If the algorithm already exists, refresh its
        classification and discovered key size.
        """

        algorithm_name = (
            data["algorithm_name"]
            .upper()
            .strip()
        )

        # ------------------------------------------------------
        # Analyze algorithm
        # ------------------------------------------------------

        analysis = (
            AlgorithmInventoryService.analyze_algorithm(
                algorithm_name
            )
        )

        # ------------------------------------------------------
        # Check for existing algorithm
        # ------------------------------------------------------

        existing = AlgorithmAsset.query.filter_by(
            algorithm_name=algorithm_name
        ).first()

        if existing:

            # Update discovered key size when available
            if data.get("key_size"):
                existing.key_size = data["key_size"]

            # Refresh classification
            existing.category = analysis["category"]
            existing.allowed = analysis["allowed"]
            existing.active = analysis["active"]
            existing.risk_level = analysis["risk_level"]
            existing.recommended_mode = analysis["recommended_mode"]
            existing.description = analysis["description"]

            # Keep existing deployment mode unless invalid
            valid_deployment_modes = [
                "CLASSICAL",
                "HYBRID",
                "PURE_PQC",
            ]

            if existing.deployment_mode not in valid_deployment_modes:
                existing.deployment_mode = (
                    analysis["recommended_mode"]
                )

            db.session.commit()

            return existing.to_dict()

        # ------------------------------------------------------
        # Validate deployment mode
        # ------------------------------------------------------

        valid_deployment_modes = [
            "CLASSICAL",
            "HYBRID",
            "PURE_PQC",
        ]

        recommended_mode = (
            analysis.get("recommended_mode")
        )

        deployment_mode = (
            recommended_mode
            if recommended_mode in valid_deployment_modes
            else "CLASSICAL"
        )

        # ------------------------------------------------------
        # Create database record
        # ------------------------------------------------------

        algorithm = AlgorithmAsset(

            algorithm_name=algorithm_name,

            category=analysis["category"],

            version=data.get("version"),

            key_size=data.get("key_size"),

            allowed=analysis["allowed"],

            active=analysis["active"],

            deployment_mode=deployment_mode,

            risk_level=analysis["risk_level"],

            recommended_mode=analysis["recommended_mode"],

            description=analysis["description"],
        )

        db.session.add(algorithm)
        db.session.commit()

        return algorithm.to_dict()

    # ==========================================================
    # AUTO REGISTER DISCOVERED ALGORITHM
    # ==========================================================

    @staticmethod
    def auto_register_algorithm(
        algorithm_name,
        key_size=None
    ):
        """
        Automatically register an algorithm discovered
        during Asset Discovery.
        """

        return AlgorithmInventoryService.create_algorithm({

            "algorithm_name": algorithm_name,

            "key_size": key_size,

            "version": "Discovered",
        })

    # ==========================================================
    # GET ALGORITHM
    # ==========================================================

    @staticmethod
    def get_algorithm_by_name(name):
        """
        Return an algorithm by name.
        """

        return AlgorithmAsset.query.filter_by(
            algorithm_name=name.upper().strip()
        ).first()

    # ==========================================================
    # SET ALLOWED
    # ==========================================================

    @staticmethod
    def set_allowed(
        algorithm_id,
        allowed
    ):

        algorithm = AlgorithmAsset.query.get_or_404(
            algorithm_id
        )

        algorithm.allowed = bool(allowed)

        db.session.commit()

        return algorithm.to_dict()

    # ==========================================================
    # SET ACTIVE
    # ==========================================================

    @staticmethod
    def set_active(
        algorithm_id,
        active
    ):

        algorithm = AlgorithmAsset.query.get_or_404(
            algorithm_id
        )

        algorithm.active = bool(active)

        db.session.commit()

        return algorithm.to_dict()

    # ==========================================================
    # SET DEPLOYMENT MODE
    # ==========================================================

    @staticmethod
    def set_deployment_mode(mode):

        mode = mode.upper()

        allowed_modes = [
            "CLASSICAL",
            "HYBRID",
            "PURE_PQC",
        ]

        if mode not in allowed_modes:

            raise ValueError(
                "Invalid deployment mode. "
                "Use CLASSICAL, HYBRID or PURE_PQC."
            )

        algorithms = AlgorithmAsset.query.all()

        for algorithm in algorithms:

            if mode == "CLASSICAL":

                algorithm.active = (
                    algorithm.allowed
                    and algorithm.category in [
                        "CLASSICAL",
                        "SYMMETRIC",
                        "HASH",
                    ]
                )

            elif mode == "HYBRID":

                algorithm.active = (
                    algorithm.allowed
                    and algorithm.category in [
                        "CLASSICAL",
                        "HYBRID",
                        "PQC_KEM",
                        "PQC_SIGNATURE",
                        "SYMMETRIC",
                        "HASH",
                    ]
                )

            elif mode == "PURE_PQC":

                algorithm.active = (
                    algorithm.allowed
                    and algorithm.category in [
                        "PQC_KEM",
                        "PQC_SIGNATURE",
                        "SYMMETRIC",
                        "HASH",
                    ]
                )

            algorithm.deployment_mode = mode

        db.session.commit()

        return {
            "message": (
                "Deployment mode updated successfully."
            ),
            "deployment_mode": mode,
        }

    # ==========================================================
    # SUMMARY
    # ==========================================================

    @staticmethod
    def get_summary():

        algorithms = AlgorithmAsset.query.all()

        return {

            "module":
                "Algorithm Inventory",

            "total_algorithms":
                len(algorithms),

            "allowed_algorithms":
                sum(
                    bool(a.allowed)
                    for a in algorithms
                ),

            "disabled_algorithms":
                sum(
                    not bool(a.allowed)
                    for a in algorithms
                ),

            "active_algorithms":
                sum(
                    bool(a.active)
                    for a in algorithms
                ),

            "classical":
                sum(
                    a.category == "CLASSICAL"
                    for a in algorithms
                ),

            "pqc":
                sum(
                    a.category.startswith("PQC")
                    for a in algorithms
                ),

            "hybrid":
                sum(
                    a.category == "HYBRID"
                    for a in algorithms
                ),

            "deployment_mode":
                (
                    algorithms[0].deployment_mode
                    if algorithms
                    else "CLASSICAL"
                ),

            "timestamp":
                datetime.utcnow().isoformat(),
         }
