from marshmallow import Schema, fields, validate


class StoreSecretSchema(Schema):

    secret_name = fields.String(
        required=True
    )

    secret_value = fields.String(
        required=True
    )

    secret_type = fields.String(
        required=True,
        validate=validate.OneOf(
            [
                "DATABASE",
                "API_KEY",
                "TLS_KEY",
                "JWT_KEY",
                "PQC_KEY",
                "CERTIFICATE",
            ]
        ),
    )
