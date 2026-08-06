from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.profile.services import ProfileService
from app.profile.schemas import (
    ProfileSchema,
    UpdateProfileSchema,
    PasswordSchema
)


profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/api/v1/profile"
)



@profile_bp.route(
    "",
    methods=["GET"]
)
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()


    user = ProfileService.get_user_profile(
        user_id
    )


    if not user:
        return jsonify({
            "error":"User not found"
        }),404



    return jsonify(
        ProfileSchema().dump(user)
    ),200





@profile_bp.route(
    "",
    methods=["PUT"]
)
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()


    data = request.get_json()


    result = UpdateProfileSchema().load(
        data
    )


    user = ProfileService.update_email(
        user_id,
        result["email"]
    )


    return jsonify({
        "message":"Profile updated",
        "email":user.email
    })





@profile_bp.route(
    "/password",
    methods=["PUT"]
)
@jwt_required()
def change_password():


    user_id = get_jwt_identity()


    data = request.get_json()


    result = PasswordSchema().load(
        data
    )


    success,message = ProfileService.change_password(
        user_id,
        result["old_password"],
        result["new_password"]
    )


    if not success:

        return jsonify({
            "error":message
        }),400



    return jsonify({
        "message":message
    })
