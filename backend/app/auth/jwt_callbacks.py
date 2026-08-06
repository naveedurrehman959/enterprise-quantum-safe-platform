from flask import jsonify
from app.extensions import jwt


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify(
        {
            "error": "Access token has expired.",
        }
    ), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify(
        {
            "error": "Invalid token.",
        }
    ), 422


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(
        {
            "error": "Authorization token is missing.",
        }
    ), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify(
        {
            "error": "Token has been revoked.",
        }
    ), 401


@jwt.needs_fresh_token_loader
def fresh_token_callback(jwt_header, jwt_payload):
    return jsonify(
        {
            "error": "Fresh token required.",
        }
    ), 401
