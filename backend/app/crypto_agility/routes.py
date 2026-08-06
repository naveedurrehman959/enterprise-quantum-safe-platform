from flask import Blueprint, jsonify, request

from app.audit.services import create_audit_log
from flask_jwt_extended import jwt_required, get_jwt_identity

from .services import CryptoAgilityService

crypto_agility_bp = Blueprint(
    "crypto_agility",
    __name__,
    url_prefix="/api/v1/crypto-agility"
)


# -----------------------------------------
# Engine Status
# -----------------------------------------

@crypto_agility_bp.route(
    "/status",
    methods=["GET"]
)
@jwt_required()
def status():

    return jsonify(
        CryptoAgilityService.get_status(
            get_jwt_identity()
        )
    )


# -----------------------------------------
# Deployment Mode
# -----------------------------------------

@crypto_agility_bp.route(
    "/deployment-mode",
    methods=["PUT"]
)
@jwt_required()
def deployment_mode():

    data = request.get_json()

    result = CryptoAgilityService.change_deployment_mode(
        data["mode"]
    )

    create_audit_log(
        user_id=get_jwt_identity(),
        action="DEPLOYMENT_MODE_CHANGED",
        module="CRYPTO_AGILITY",
        status="SUCCESS",
        description=f"Deployment mode changed to {data['mode']}"
    )

    return jsonify(result)


# -----------------------------------------
# Recommend Migration
# -----------------------------------------

@crypto_agility_bp.route(
    "/recommend",
    methods=["POST"]
)
@jwt_required()
def recommend():

    data = request.get_json()

    return jsonify(

        CryptoAgilityService.recommend_migration(

            data["algorithm"],

            get_jwt_identity()

        )

    )


# -----------------------------------------
# Validate Algorithm
# -----------------------------------------

@crypto_agility_bp.route(
    "/validate",
    methods=["POST"]
)
@jwt_required()
def validate():

    data = request.get_json()

    return jsonify(

        CryptoAgilityService.validate_algorithm(

            data["algorithm"]

        )

    )


# -----------------------------------------
# Inventory
# -----------------------------------------

@crypto_agility_bp.route(
    "/inventory",
    methods=["GET"]
)
@jwt_required()
def inventory():

    return jsonify(

        CryptoAgilityService.inventory()

    )
