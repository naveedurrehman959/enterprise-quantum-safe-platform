# backend/app/auth/schemas.py

from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    """
    User registration schema.
    """

    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
    )

    email = fields.Email(
        required=True,
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
    )


class LoginSchema(Schema):
    """
    User login schema.
    """

    email = fields.Email(
        required=True,
    )

    password = fields.Str(
        required=True,
    )
