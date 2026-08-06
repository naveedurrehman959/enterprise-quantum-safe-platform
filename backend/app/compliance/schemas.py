# backend/app/compliance/schemas.py

from marshmallow import Schema, fields, validate


class ComplianceFrameworkSchema(Schema):

    framework = fields.String(
        required=True,
        validate=validate.OneOf(
            [
                "NIST-PQC",
                "NIST-CSF-2.0",
                "CNSA-2.0",
                "ISO-27001",
                "PCI-DSS",
            ]
        ),
    )
