# backend/app/auth/logout.py

from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
)

from app.extensions import db
from app.models.token_blocklist import TokenBlocklist
from app.audit.services import create_audit_log


@jwt_required(verify_type=False)
def logout():

    # Get token information
    token = get_jwt()

    jti = token["jti"]
    token_type = token["type"]
    user_id = get_jwt_identity()

    # Add token to blocklist
    revoked_token = TokenBlocklist(
        jti=jti,
        token_type=token_type,
    )

    db.session.add(revoked_token)

    # Create audit log entry
    create_audit_log(
        user_id=user_id,
        action="LOGOUT",
        module="AUTH",
        status="SUCCESS",
        description=f"{token_type} token revoked successfully.",
    )

    # Commit all changes
    db.session.commit()

    # Return response
    return jsonify(
        {
            "message": f"{token_type} token revoked successfully."
        }
    ), 200
