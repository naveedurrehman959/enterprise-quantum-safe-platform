from app import create_app, db
from app.algorithm_inventory.models import AlgorithmAsset

app = create_app()

ALGORITHMS = [
    {
        "algorithm_name": "RSA-2048",
        "category": "CLASSICAL",
        "version": "1.0",
        "key_size": 2048,
        "allowed": True,
        "active": True,
        "deployment_mode": "CLASSICAL",
        "risk_level": "CRITICAL",
        "recommended_mode": "HYBRID",
        "description": "Legacy public-key encryption"
    },
    {
        "algorithm_name": "ECDHE",
        "category": "CLASSICAL",
        "version": "1.0",
        "key_size": 256,
        "allowed": True,
        "active": True,
        "deployment_mode": "CLASSICAL",
        "risk_level": "HIGH",
        "recommended_mode": "HYBRID",
        "description": "Elliptic Curve Diffie-Hellman"
    },
    {
        "algorithm_name": "ECDSA",
        "category": "CLASSICAL",
        "version": "1.0",
        "key_size": 256,
        "allowed": True,
        "active": True,
        "deployment_mode": "CLASSICAL",
        "risk_level": "HIGH",
        "recommended_mode": "HYBRID",
        "description": "Elliptic Curve Digital Signature"
    },
    {
        "algorithm_name": "ML-KEM-768",
        "category": "PQC_KEM",
        "version": "FIPS-203",
        "key_size": 768,
        "allowed": True,
        "active": True,
        "deployment_mode": "HYBRID",
        "risk_level": "SAFE",
        "recommended_mode": "PURE_PQC",
        "description": "NIST standardized key encapsulation"
    },
    {
        "algorithm_name": "ML-KEM-1024",
        "category": "PQC_KEM",
        "version": "FIPS-203",
        "key_size": 1024,
        "allowed": True,
        "active": True,
        "deployment_mode": "PURE_PQC",
        "risk_level": "SAFE",
        "recommended_mode": "PURE_PQC",
        "description": "High security PQC KEM"
    },
    {
        "algorithm_name": "ML-DSA-65",
        "category": "PQC_SIGNATURE",
        "version": "FIPS-204",
        "key_size": 65,
        "allowed": True,
        "active": True,
        "deployment_mode": "PURE_PQC",
        "risk_level": "SAFE",
        "recommended_mode": "PURE_PQC",
        "description": "Post-Quantum Digital Signature"
    },
    {
        "algorithm_name": "ML-DSA-87",
        "category": "PQC_SIGNATURE",
        "version": "FIPS-204",
        "key_size": 87,
        "allowed": True,
        "active": True,
        "deployment_mode": "PURE_PQC",
        "risk_level": "SAFE",
        "recommended_mode": "PURE_PQC",
        "description": "High security PQC signature"
    },
    {
        "algorithm_name": "AES-256-GCM",
        "category": "SYMMETRIC",
        "version": "NIST",
        "key_size": 256,
        "allowed": True,
        "active": True,
        "deployment_mode": "HYBRID",
        "risk_level": "SAFE",
        "recommended_mode": "PURE_PQC",
        "description": "Authenticated symmetric encryption"
    },
    {
        "algorithm_name": "SHA3-512",
        "category": "HASH",
        "version": "SHA-3",
        "key_size": 512,
        "allowed": True,
        "active": True,
        "deployment_mode": "HYBRID",
        "risk_level": "SAFE",
        "recommended_mode": "PURE_PQC",
        "description": "Secure hash algorithm"
    },
    {
        "algorithm_name": "RSA + ML-KEM",
        "category": "HYBRID",
        "version": "Hybrid",
        "key_size": 2048,
        "allowed": True,
        "active": True,
        "deployment_mode": "HYBRID",
        "risk_level": "LOW",
        "recommended_mode": "HYBRID",
        "description": "Hybrid migration mode"
    }
]
with app.app_context():

    for item in ALGORITHMS:

        existing = AlgorithmAsset.query.filter_by(
            algorithm_name=item["algorithm_name"]
        ).first()

        if not existing:
            db.session.add(
                AlgorithmAsset(**item)
            )

    db.session.commit()

    print("Inventory synchronized successfully.")
