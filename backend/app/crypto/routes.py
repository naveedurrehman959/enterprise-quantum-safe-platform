# backend/app/crypto/routes.py

from flask import Blueprint, jsonify, request

from flask_jwt_extended import jwt_required, get_jwt_identity

from app.auth.decorators import roles_required


crypto_bp = Blueprint(
    "crypto",
    __name__,
    url_prefix="/api/v1/crypto",
)


# ---------------------------------
# View Available Algorithms
# ---------------------------------

@crypto_bp.route("/algorithms", methods=["GET"])
@roles_required("user", "security", "admin")
def list_algorithms():

    return jsonify(
        {
            "algorithms": [
                {
                    "name": "ML-KEM-768",
                    "type": "Key Encapsulation Mechanism",
                    "status": "enabled"
                },
                {
                    "name": "ML-DSA-65",
                    "type": "Digital Signature",
                    "status": "enabled"
                },
                {
                    "name": "AES-256-GCM",
                    "type": "Symmetric Encryption",
                    "status": "enabled"
                }
            ]
        }
    ), 200



# ---------------------------------
# Deploy PQC Algorithm
# Security/Admin Only
# ---------------------------------

@crypto_bp.route("/deploy", methods=["POST"])
@roles_required("security_analyst", "admin")
def deploy_algorithm():

    data = request.get_json()

    algorithm = data.get(
        "algorithm"
    )

    return jsonify(
        {
            "message": "Algorithm deployment successful",
            "algorithm": algorithm
        }
    ), 200



# ---------------------------------
# Crypto Status
# ---------------------------------

@crypto_bp.route("/status", methods=["GET"])
@roles_required("user", "security_analyst", "admin")
def crypto_status():

    return jsonify(
        {
            "crypto_engine": "active",
            "pqc_enabled": True,
            "hybrid_mode": True
        }
    ), 200
