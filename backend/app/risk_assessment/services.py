# backend/app/risk_assessment/services.py

from datetime import datetime

from app.algorithm_inventory.models import AlgorithmAsset


class RiskAssessmentService:
    """
    Enterprise Quantum Risk Assessment Engine

    Responsibilities
    ----------------
    • Algorithm risk analysis
    • Asset Discovery integration
    • TLS security assessment
    • Certificate expiry assessment
    • Enterprise inventory reporting
    """

    # ============================================================
    # Algorithm Risk Database
    # ============================================================

    RISK_DATABASE = {

        # --------------------------------------------------------
        # Generic Algorithms (used by Asset Discovery)
        # --------------------------------------------------------

        "RSA": {
            "category": "ASYMMETRIC_ENCRYPTION",
            "risk_level": "HIGH",
            "risk_score": 85,
            "quantum_vulnerable": True,
            "recommendation": "Deploy Hybrid TLS using ML-KEM",
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

        "ECC": {
            "category": "DIGITAL_SIGNATURE",
            "risk_level": "HIGH",
            "risk_score": 90,
            "quantum_vulnerable": True,
            "recommendation": "Replace with ML-DSA",
            "recommended_algorithm": "ML-DSA-65",
        },

        "EC": {
            "category": "DIGITAL_SIGNATURE",
            "risk_level": "HIGH",
            "risk_score": 90,
            "quantum_vulnerable": True,
            "recommendation": "Replace with ML-DSA",
            "recommended_algorithm": "ML-DSA-65",
        },

        "ED25519": {
            "category": "MODERN_SIGNATURE",
            "risk_level": "MEDIUM",
            "risk_score": 45,
            "quantum_vulnerable": True,
            "recommendation": "Plan migration to ML-DSA",
            "recommended_algorithm": "ML-DSA-65",
        },

        "ED448": {
            "category": "MODERN_SIGNATURE",
            "risk_level": "MEDIUM",
            "risk_score": 40,
            "quantum_vulnerable": True,
            "recommendation": "Plan migration to ML-DSA",
            "recommended_algorithm": "ML-DSA-65",
        },

        # --------------------------------------------------------
        # Classical Algorithms
        # --------------------------------------------------------

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
            "recommendation": "Deploy Hybrid TLS",
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

        "ECDHE": {
            "category": "KEY_EXCHANGE",
            "risk_level": "HIGH",
            "risk_score": 80,
            "quantum_vulnerable": True,
            "recommendation": "Enable Hybrid TLS",
            "recommended_algorithm": "ECDHE + ML-KEM-768",
        },

        # --------------------------------------------------------
        # Symmetric
        # --------------------------------------------------------

        "AES": {
            "category": "SYMMETRIC_ENCRYPTION",
            "risk_level": "SAFE",
            "risk_score": 10,
            "quantum_vulnerable": False,
            "recommendation": "Approved",
            "recommended_algorithm": "AES-256-GCM",
        },

        "AES-128": {
            "category": "SYMMETRIC_ENCRYPTION",
            "risk_level": "MEDIUM",
            "risk_score": 50,
            "quantum_vulnerable": True,
            "recommendation": "Upgrade to AES-256",
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

        # --------------------------------------------------------
        # Hashing
        # --------------------------------------------------------

        "SHA": {
            "category": "HASH",
            "risk_level": "SAFE",
            "risk_score": 10,
            "quantum_vulnerable": False,
            "recommendation": "Approved",
            "recommended_algorithm": "SHA-256",
        },

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
            "recommendation": "Quantum Resistant",
            "recommended_algorithm": "SHA3-512",
        },

        # --------------------------------------------------------
        # Post Quantum Cryptography
        # --------------------------------------------------------

        "ML-KEM": {
            "category": "PQC_KEM",
            "risk_level": "SAFE",
            "risk_score": 0,
            "quantum_vulnerable": False,
            "recommendation": "Approved",
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
            "recommendation": "Approved",
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

    # ============================================================
    # TLS Version Risk
    # ============================================================

    TLS_RISK = {
        "TLSv1": ("CRITICAL", 100),
        "TLSv1.1": ("HIGH", 80),
        "TLSv1.2": ("MEDIUM", 40),
        "TLSv1.3": ("SAFE", 0),
    }

    @staticmethod
    def get_status():

        return {
            "engine": "ACTIVE",
            "version": "2.0",
            "quantum_threat_detection": "ENABLED",
            "tls_assessment": "ENABLED",
            "certificate_assessment": "ENABLED",
            "asset_discovery": "ENABLED",
            "risk_database": "LOADED",
            "timestamp": datetime.utcnow().isoformat()
        }

    @classmethod
    def _find_algorithm(cls, algorithm: str):
        """
        Find the best matching algorithm definition.
        """

        algorithm = algorithm.upper().strip()

        # Exact match first
        if algorithm in cls.RISK_DATABASE:
            return cls.RISK_DATABASE[algorithm]

        # Partial match
        for key, value in cls.RISK_DATABASE.items():
            if key in algorithm:
                return value

        return None
        @classmethod
    def assess_algorithm(cls, algorithm):
        """
        Assess a cryptographic algorithm and determine its
        quantum risk.
        """

        algorithm = algorithm.upper().strip()

        risk = cls._find_algorithm(algorithm)

        if risk:

            migration_required = (
                risk["risk_level"] != "SAFE"
            )

            if risk["risk_level"] == "CRITICAL":
                decision = "BLOCKED"

            elif migration_required:
                decision = "MIGRATION_REQUIRED"

            else:
                decision = "APPROVED"

            return {

                "algorithm": algorithm,

                **risk,

                "migration_required":
                    migration_required,

                "decision":
                    decision

            }

        return {

            "algorithm": algorithm,

            "category": "UNKNOWN",

            "risk_level": "UNKNOWN",

            "risk_score": 50,

            "quantum_vulnerable": True,

            "migration_required": True,

            "decision": "MANUAL_REVIEW",

            "recommendation":
                "Manual security review required.",

            "recommended_algorithm":
                None

        }

    @classmethod
    def assess_tls_version(cls, tls_version):
        """
        Assess TLS protocol version.
        """

        if not tls_version:

            return {

                "tls_version": "UNKNOWN",

                "risk_level": "UNKNOWN",

                "risk_score": 50

            }

        level, score = cls.TLS_RISK.get(

            tls_version,

            ("UNKNOWN", 50)

        )

        return {

            "tls_version": tls_version,

            "risk_level": level,

            "risk_score": score

        }

    @staticmethod
    def assess_certificate_expiry(valid_to):
        """
        Evaluate certificate expiry.
        """

        if valid_to is None:

            return {

                "status": "UNKNOWN",

                "days_remaining": None,

                "risk_level": "UNKNOWN"

            }

        now = datetime.utcnow()

        days_remaining = (
            valid_to - now
        ).days

        if days_remaining < 0:

            return {

                "status": "EXPIRED",

                "days_remaining":
                    days_remaining,

                "risk_level":
                    "CRITICAL"

            }

        if days_remaining <= 30:

            return {

                "status": "EXPIRING_SOON",

                "days_remaining":
                    days_remaining,

                "risk_level":
                    "HIGH"

            }

        if days_remaining <= 90:

            return {

                "status": "WARNING",

                "days_remaining":
                    days_remaining,

                "risk_level":
                    "MEDIUM"

            }

        return {

            "status": "VALID",

            "days_remaining":
                days_remaining,

            "risk_level":
                "SAFE"

        }

    @classmethod
    def assess_asset(cls, asset):
        """
        Enterprise Asset Discovery Assessment.

        Accepts a DiscoveredAsset model and
        returns a complete security assessment.
        """

        algorithm_result = cls.assess_algorithm(
            asset.public_key_algorithm
        )

        tls_result = cls.assess_tls_version(
            asset.tls_version
        )

        certificate_result = cls.assess_certificate_expiry(
            asset.valid_to
        )

        highest = max(
            algorithm_result["risk_score"],
            tls_result["risk_score"]
        )

        overall = "SAFE"

        if highest >= 90:
            overall = "CRITICAL"

        elif highest >= 70:
            overall = "HIGH"

        elif highest >= 40:
            overall = "MEDIUM"

        return {

            "hostname":
                asset.hostname,

            "ip_address":
                asset.ip_address,

            "algorithm":
                algorithm_result,

            "tls":
                tls_result,

            "certificate":
                certificate_result,

            "overall_risk":
                overall,

            "overall_score":
                highest,

            "recommendation":
                algorithm_result.get(
                    "recommended_algorithm"
                )

        }
            @classmethod
    def assess_inventory(cls):
        """
        Assess all registered algorithms in the inventory.
        """

        assets = AlgorithmAsset.query.all()

        result = {
            "total_assets": len(assets),
            "critical_risk": 0,
            "high_risk": 0,
            "medium_risk": 0,
            "low_risk": 0,
            "safe_assets": 0,
            "migration_required": 0,
            "approved": 0,
            "blocked": 0,
        }

        for asset in assets:

            risk = cls.assess_algorithm(
                asset.algorithm_name
            )

            level = risk["risk_level"]

            if level == "CRITICAL":
                result["critical_risk"] += 1

            elif level == "HIGH":
                result["high_risk"] += 1

            elif level == "MEDIUM":
                result["medium_risk"] += 1

            elif level == "LOW":
                result["low_risk"] += 1

            elif level == "SAFE":
                result["safe_assets"] += 1

            if risk["migration_required"]:
                result["migration_required"] += 1

            if risk["decision"] == "APPROVED":
                result["approved"] += 1

            elif risk["decision"] == "BLOCKED":
                result["blocked"] += 1

        result["quantum_readiness_score"] = cls.calculate_quantum_readiness(
            result
        )

        result["timestamp"] = datetime.utcnow().isoformat()

        return result

    @classmethod
    def inventory(cls):
        """
        Return the algorithm inventory grouped by risk.
        """

        vulnerable = []
        quantum_safe = []

        for algorithm, data in cls.RISK_DATABASE.items():

            entry = {
                "algorithm": algorithm,
                **data
            }

            if data["quantum_vulnerable"]:
                vulnerable.append(entry)
            else:
                quantum_safe.append(entry)

        return {

            "total_algorithms":
                len(cls.RISK_DATABASE),

            "vulnerable_algorithms":
                vulnerable,

            "quantum_safe_algorithms":
                quantum_safe

        }

    @staticmethod
    def calculate_quantum_readiness(summary):
        """
        Calculate a readiness score from 0-100.
        """

        total = summary["total_assets"]

        if total == 0:
            return 100

        penalty = (
            summary["critical_risk"] * 30 +
            summary["high_risk"] * 20 +
            summary["medium_risk"] * 10 +
            summary["low_risk"] * 5
        )

        score = 100 - (penalty / total)

        return round(max(score, 0), 2)

    @classmethod
    def dashboard_summary(cls):
        """
        Dashboard summary for frontend widgets.
        """

        assessment = cls.assess_inventory()

        return {

            "engine": "ACTIVE",

            "overall_status":
                "HEALTHY"
                if assessment["critical_risk"] == 0
                else "AT_RISK",

            "quantum_readiness_score":
                assessment["quantum_readiness_score"],

            "critical_assets":
                assessment["critical_risk"],

            "high_risk_assets":
                assessment["high_risk"],

            "safe_assets":
                assessment["safe_assets"],

            "migration_required":
                assessment["migration_required"],

            "last_updated":
                datetime.utcnow().isoformat()

        }

