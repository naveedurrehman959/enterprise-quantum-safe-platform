# backend/app/crypto/algorithm_registry.py

"""
Quantum-Safe Algorithm Registry

Central database for cryptographic algorithm classification
and PQC migration recommendations.

Used by:
- Risk Assessment Engine
- Policy Engine
- Migration Engine
- Crypto Agility Framework
"""


ALGORITHMS = {

    # -----------------------------
    # Classical Asymmetric Algorithms
    # -----------------------------

    "RSA-2048": {

        "category": "ASYMMETRIC_ENCRYPTION",

        "security_level": "VULNERABLE",

        "quantum_vulnerable": True,

        "risk_level": "CRITICAL",

        "replacement": [
            "ML-KEM-768",
            "ML-DSA-65"
        ],

        "migration_strategy":
            "HYBRID_MIGRATION",

        "description":
            "RSA is vulnerable to Shor's algorithm."
    },


    "RSA-3072": {

        "category": "ASYMMETRIC_ENCRYPTION",

        "security_level": "VULNERABLE",

        "quantum_vulnerable": True,

        "risk_level": "CRITICAL",

        "replacement": [
            "ML-KEM-768",
            "ML-DSA-65"
        ],

        "migration_strategy":
            "HYBRID_MIGRATION",

        "description":
            "RSA requires migration before cryptographically relevant quantum computers."
    },


    # -----------------------------
    # Elliptic Curve Algorithms
    # -----------------------------

    "ECDHE": {

        "category": "KEY_EXCHANGE",

        "security_level": "VULNERABLE",

        "quantum_vulnerable": True,

        "risk_level": "HIGH",

        "replacement": [
            "ML-KEM-768"
        ],

        "migration_strategy":
            "HYBRID_TLS_MIGRATION",

        "description":
            "ECDHE key exchange is vulnerable to quantum attacks."
    },


    "ECDSA": {

        "category": "DIGITAL_SIGNATURE",

        "security_level": "VULNERABLE",

        "quantum_vulnerable": True,

        "risk_level": "HIGH",

        "replacement": [
            "ML-DSA-65"
        ],

        "migration_strategy":
            "HYBRID_SIGNATURE_MIGRATION",

        "description":
            "ECDSA signatures can be broken using Shor's algorithm."
    },


    "Ed25519": {

        "category": "DIGITAL_SIGNATURE",

        "security_level": "VULNERABLE",

        "quantum_vulnerable": True,

        "risk_level": "HIGH",

        "replacement": [
            "ML-DSA-65"
        ],

        "migration_strategy":
            "HYBRID_SIGNATURE_MIGRATION",

        "description":
            "Ed25519 requires PQC signature migration."
    },


    # -----------------------------
    # Symmetric Algorithms
    # -----------------------------

    "AES-128": {

        "category": "SYMMETRIC_ENCRYPTION",

        "security_level": "REDUCED",

        "quantum_vulnerable": True,

        "risk_level": "MEDIUM",

        "replacement": [
            "AES-256"
        ],

        "migration_strategy":
            "KEY_SIZE_UPGRADE",

        "description":
            "AES-128 security is reduced by Grover's algorithm."
    },


    "AES-256-GCM": {

        "category": "SYMMETRIC_ENCRYPTION",

        "security_level": "QUANTUM_SAFE",

        "quantum_vulnerable": False,

        "risk_level": "SAFE",

        "replacement": [],

        "migration_strategy":
            "NO_MIGRATION_REQUIRED",

        "description":
            "AES-256 remains secure against quantum attacks."
    },


    # -----------------------------
    # NIST PQC Approved Algorithms
    # -----------------------------

    "ML-KEM-512": {

        "category": "PQC_KEY_ENCAPSULATION",

        "security_level": "QUANTUM_SAFE",

        "quantum_vulnerable": False,

        "risk_level": "SAFE",

        "replacement": [],

        "migration_strategy":
            "NO_MIGRATION_REQUIRED",

        "description":
            "NIST approved post-quantum KEM."
    },


    "ML-KEM-768": {

        "category": "PQC_KEY_ENCAPSULATION",

        "security_level": "QUANTUM_SAFE",

        "quantum_vulnerable": False,

        "risk_level": "SAFE",

        "replacement": [],

        "migration_strategy":
            "NO_MIGRATION_REQUIRED",

        "description":
            "Recommended enterprise PQC key encapsulation mechanism."
    },


    "ML-KEM-1024": {

        "category": "PQC_KEY_ENCAPSULATION",

        "security_level": "QUANTUM_SAFE",

        "quantum_vulnerable": False,

        "risk_level": "SAFE",

        "replacement": [],

        "migration_strategy":
            "NO_MIGRATION_REQUIRED",

        "description":
            "High security PQC KEM."
    },


    "ML-DSA-65": {

        "category": "PQC_DIGITAL_SIGNATURE",

        "security_level": "QUANTUM_SAFE",

        "quantum_vulnerable": False,

        "risk_level": "SAFE",

        "replacement": [],

        "migration_strategy":
            "NO_MIGRATION_REQUIRED",

        "description":
            "NIST approved post-quantum digital signature."
    }

}


def get_algorithm_details(algorithm):

    """
    Return algorithm metadata.
    """

    return ALGORITHMS.get(
        algorithm,
        {
            "category": "UNKNOWN",
            "security_level": "UNKNOWN",
            "quantum_vulnerable": None,
            "risk_level": "UNKNOWN",
            "replacement": [],
            "migration_strategy": "MANUAL_REVIEW",
            "description":
                "Algorithm not found in registry."
        }
    )


def is_quantum_safe(algorithm):

    """
    Check whether algorithm is quantum safe.
    """

    details = get_algorithm_details(
        algorithm
    )

    return details.get(
        "quantum_vulnerable"
    ) is False
