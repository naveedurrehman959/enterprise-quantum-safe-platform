# backend/app/crypto/services.py

from app.audit.services import create_audit_log


def get_crypto_status(user_id=None):
    """
    Return the current status of the crypto engine.
    """

    create_audit_log(
        user_id=user_id,
        action="VIEW_CRYPTO_STATUS",
        module="CRYPTO",
        status="SUCCESS",
        description="Viewed crypto engine status.",
    )

    return {
        "crypto_engine": "active",
        "pqc_enabled": True,
        "hybrid_mode": True,
    }


def get_supported_algorithms(user_id=None):
    """
    Return all supported cryptographic algorithms.
    """

    create_audit_log(
        user_id=user_id,
        action="VIEW_ALGORITHMS",
        module="CRYPTO",
        status="SUCCESS",
        description="Viewed supported cryptographic algorithms.",
    )

    return {
        "algorithms": [
            {
                "name": "ML-KEM-768",
                "type": "Key Encapsulation Mechanism",
                "status": "enabled",
            },
            {
                "name": "ML-KEM-1024",
                "type": "Key Encapsulation Mechanism",
                "status": "enabled",
            },
            {
                "name": "ML-DSA-65",
                "type": "Digital Signature",
                "status": "enabled",
            },
            {
                "name": "ML-DSA-87",
                "type": "Digital Signature",
                "status": "enabled",
            },
            {
                "name": "AES-256-GCM",
                "type": "Symmetric Encryption",
                "status": "enabled",
            },
            {
                "name": "HKDF",
                "type": "Key Derivation Function",
                "status": "enabled",
            },
        ]
    }


def deploy_crypto_algorithm(algorithm, user_id=None):
    """
    Simulate cryptographic algorithm deployment.
    """

    create_audit_log(
        user_id=user_id,
        action="DEPLOY_ALGORITHM",
        module="CRYPTO",
        status="SUCCESS",
        description=f"Deployed algorithm: {algorithm}",
    )

    return {
        "message": "Algorithm deployment successful.",
        "algorithm": algorithm,
        "deployment_status": "active",
        "hybrid_mode": True,
    }
