from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    get_jwt_identity,
)

from app.auth.decorators import (
    roles_required,
)

from .schemas import (
    StoreSecretSchema,
)

from .services import (
    get_vault_status,
    store_secret,
    get_secret,
    delete_secret,
    list_secrets,
)


vault_bp = Blueprint(
    "vault",
    __name__,
    url_prefix="/api/v1/vault",
)


@vault_bp.route("/status", methods=["GET"])
@roles_required(
    "user",
    "security",
    "admin",
)
def vault_status():

    user_id = get_jwt_identity()

    return jsonify(
        get_vault_status(user_id)
    ), 200


@vault_bp.route(
    "/store-secret",
    methods=["POST"],
)
@roles_required(
    "security",
    "admin",
)
def store_secret_route():

    data = request.get_json()

    errors = (
        StoreSecretSchema()
        .validate(data)
    )

    if errors:
        return jsonify(errors), 400

    user_id = get_jwt_identity()

    return jsonify(
        store_secret(
            data["secret_name"],
            data["secret_value"],
            data["secret_type"],
            user_id,
        )
    ), 200


@vault_bp.route(
    "/get-secret/<secret_name>",
    methods=["GET"],
)
@roles_required(
    "security",
    "admin",
)
def get_secret_route(secret_name):

    user_id = get_jwt_identity()

    return jsonify(
        get_secret(
            secret_name,
            user_id,
        )
    ), 200


@vault_bp.route(
    "/delete-secret/<secret_name>",
    methods=["DELETE"],
)
@roles_required(
    "admin",
)
def delete_secret_route(secret_name):

    user_id = get_jwt_identity()

    return jsonify(
        delete_secret(
            secret_name,
            user_id,
        )
    ), 200


@vault_bp.route(
    "/list-secrets",
    methods=["GET"],
)
@roles_required(
    "security",
    "admin",
)
def list_secrets_route():

    user_id = get_jwt_identity()

    return jsonify(
        list_secrets(
            user_id
        )
    ), 200
