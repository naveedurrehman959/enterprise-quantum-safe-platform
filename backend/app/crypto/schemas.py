# backend/app/crypto/schemas.py

from marshmallow import Schema, fields, validate


class DeployAlgorithmSchema(Schema):
    """
    Validate algorithm deployment requests.
    """

    algorithm = fields.String(
        required=True,
        validate=validate.OneOf(
            [
                "ML-KEM-768",
                "ML-KEM-1024",
                "ML-DSA-65",
                "ML-DSA-87",
                "AES-256-GCM",
                "HKDF",
            ]
        ),
    )
