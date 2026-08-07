"""
Asset Discovery Schemas
-----------------------
Marshmallow schemas for request validation and API serialization.
"""

from marshmallow import Schema, fields, validate


class ScanRequestSchema(Schema):
    """
    Request payload for scanning a host.
    """

    target = fields.String(
        required=True,
        validate=validate.Length(min=1, max=255),
        metadata={
            "description": "Hostname or IP address"
        }
    )

    port = fields.Integer(
        load_default=443,
        validate=validate.Range(min=1, max=65535),
        metadata={
            "description": "Target TLS port"
        }
    )


class AssetSchema(Schema):
    """
    Asset serialization schema.
    """

    id = fields.Integer(dump_only=True)

    hostname = fields.String()
    ip_address = fields.String()
    port = fields.Integer()

    tls_version = fields.String()
    cipher_suite = fields.String()

    public_key_algorithm = fields.String()
    key_size = fields.Integer()
    signature_algorithm = fields.String()

    issuer = fields.String()
    subject = fields.String()
    serial_number = fields.String()

    fingerprint_sha256 = fields.String()

    valid_from = fields.DateTime()
    valid_to = fields.DateTime()

    risk_level = fields.String()
    scan_status = fields.String()
    scan_error = fields.String()

    last_scanned = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ScanResponseSchema(Schema):
    """
    Standard API response after scanning.
    """

    success = fields.Boolean()

    message = fields.String()

    asset = fields.Nested(AssetSchema)
