# backend/app/crypto_agility/schemas.py

from marshmallow import Schema, fields, validate


class MigrateAlgorithmSchema(Schema):

    source_algorithm = fields.String(
        required=True
    )

    target_algorithm = fields.String(
        required=True
    )


class SwitchAlgorithmSchema(Schema):

    algorithm = fields.String(
        required=True,
        validate=validate.OneOf(
            [
                "ML-KEM-768",
                "ML-KEM-1024",
                "ML-DSA-65",
                "ML-DSA-87",
                "RSA-2048",
                "ECDHE",
                "AES-256-GCM",
                "HKDF",
            ]
        ),
    )
