# backend/app/auth/routes.py

from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
)

from app.extensions import db, limiter
from app.models.user import User

from app.auth.services import (
    register_user,
    login_user,
)

from app.auth.schemas import (
    RegisterSchema,
    LoginSchema,
)

from app.auth.logout import logout
from app.auth.decorators import roles_required


# Create Authentication Blueprint
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth",
)


# -------------------------
# Register User
# -------------------------

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():

    data = request.get_json()

    errors = RegisterSchema().validate(data)

    if errors:
        return jsonify(errors), 400

    response, status_code = register_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )

    return jsonify(response), status_code


# -------------------------
# Login User
# -------------------------

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():

    data = request.get_json()

    errors = LoginSchema().validate(data)

    if errors:
        return jsonify(errors), 400

    response, status_code = login_user(
        email=data["email"],
        password=data["password"],
    )

    return jsonify(response), status_code


# -------------------------
# User Profile
# -------------------------

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def profile():

    user_id = get_jwt_identity()

    user = db.session.get(
        User,
        int(user_id)
    )

    if not user:

        return jsonify(
            {
                "error": "User not found"
            }
        ), 404


    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }
    ), 200



# -------------------------
# Refresh Access Token
# -------------------------

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@limiter.limit("10 per minute")
def refresh():

    user_id = get_jwt_identity()

    user = db.session.get(
        User,
        int(user_id)
    )

    if not user:

        return jsonify(
            {
                "error": "User not found"
            }
        ), 404


    access_token = create_access_token(
        identity=str(user.id),
        fresh=False,
        additional_claims={
            "role": user.role
        }
    )


    return jsonify(
        {
            "access_token": access_token
        }
    ), 200



# -------------------------
# Admin RBAC Test
# -------------------------

@auth_bp.route("/admin-test", methods=["GET"])
@jwt_required()
@roles_required("admin")
def admin_test():

    return jsonify(
        {
            "message": "Admin access granted"
        }
    ), 200



# -------------------------
# Logout
# -------------------------

@auth_bp.route("/logout", methods=["POST"])
def logout_endpoint():

    return logout()
