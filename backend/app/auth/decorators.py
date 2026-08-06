# backend/app/auth/decorators.py

from functools import wraps

from flask import jsonify

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt,
)


def roles_required(*allowed_roles):
    """
    Role-Based Access Control decorator.
    """

    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):

            # Validate JWT
            verify_jwt_in_request()

            # Extract JWT claims
            claims = get_jwt()

            # Extract role
            user_role = claims.get("role")

            # Authorization check
            if user_role not in allowed_roles:

                return jsonify(
                    {
                        "error": "Insufficient permissions."
                    }
                ), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper
