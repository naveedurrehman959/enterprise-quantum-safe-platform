# backend/app/auth/services.py

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)

from app.extensions import db
from app.models.user import User
from app.auth.utils import (
    hash_password,
    verify_password,
)
from app.audit.services import create_audit_log


def register_user(username, email, password):
    """
    Register a new user.
    """

    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 400

    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 400

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )

    db.session.add(user)
    db.session.flush()

    create_audit_log(
        user_id=user.id,
        action="REGISTER",
        module="AUTH",
        status="SUCCESS",
        description=f"New user registered: {username}",
    )

    db.session.commit()

    return {
        "message": "User registered successfully."
    }, 201


def login_user(email, password):
    """
    Authenticate user.
    """

    user = User.query.filter_by(email=email).first()

    # Invalid email
    if not user:

        create_audit_log(
            user_id=None,
            action="FAILED_LOGIN",
            module="AUTH",
            status="FAILED",
            description=f"Failed login attempt for {email}",
        )

        db.session.commit()

        return {"error": "Invalid credentials"}, 401

    # Invalid password
    if not verify_password(password, user.password_hash):

        create_audit_log(
            user_id=user.id,
            action="FAILED_LOGIN",
            module="AUTH",
            status="FAILED",
            description=(
                f"Failed login attempt for {email}"
            ),
        )

        db.session.commit()

        return {"error": "Invalid credentials"}, 401

    # Successful login

    create_audit_log(
        user_id=user.id,
        action="LOGIN",
        module="AUTH",
        status="SUCCESS",
        description=(
            f"User {user.username} logged in successfully."
        ),
    )

    db.session.commit()

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        },
    )

    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        },
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "username": user.username,
        "role": user.role,
    }, 200
