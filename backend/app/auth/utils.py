# backend/app/auth/utils.py

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


def hash_password(password):
    """
    Hash a user's password.
    """
    return generate_password_hash(password)


def verify_password(password, password_hash):
    """
    Verify a user's password.
    """
    return check_password_hash(
        password_hash,
        password
    )
