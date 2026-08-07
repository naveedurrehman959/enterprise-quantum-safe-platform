from datetime import datetime

from app import db


class DiscoveredAsset(db.Model):

    __tablename__ = "discovered_assets"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    hostname = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )


    ip_address = db.Column(
        db.String(50),
        nullable=False
    )


    port = db.Column(
        db.Integer,
        nullable=False,
        default=443
    )


    tls_version = db.Column(
        db.String(20)
    )


    cipher_suite = db.Column(
        db.String(150)
    )


    public_key_algorithm = db.Column(
        db.String(50)
    )


    key_size = db.Column(
        db.Integer
    )


    signature_algorithm = db.Column(
        db.String(100)
    )


    issuer = db.Column(
        db.String(255)
    )


    subject = db.Column(
        db.String(255)
    )


    serial_number = db.Column(
        db.String(255)
    )


    fingerprint_sha256 = db.Column(
        db.String(128),
        unique=True
    )


    valid_from = db.Column(
        db.DateTime
    )


    valid_to = db.Column(
        db.DateTime
    )


    # Risk Assessment

    risk_level = db.Column(
        db.String(20),
        default="UNKNOWN"
    )


    risk_score = db.Column(
        db.Integer,
        default=0
    )


    # Policy Engine

    policy_decision = db.Column(
        db.String(50),
        default="UNKNOWN"
    )


    # Migration Engine

    migration_required = db.Column(
        db.Boolean,
        default=False
    )


    recommended_algorithm = db.Column(
        db.String(100)
    )


    scan_status = db.Column(
        db.String(20),
        default="SUCCESS"
    )


    scan_error = db.Column(
        db.Text
    )


    last_scanned = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    def to_dict(self):

        return {

            "id": self.id,

            "hostname": self.hostname,

            "ip_address": self.ip_address,

            "port": self.port,

            "tls_version": self.tls_version,

            "cipher_suite": self.cipher_suite,

            "public_key_algorithm":
                self.public_key_algorithm,

            "key_size": self.key_size,

            "signature_algorithm":
                self.signature_algorithm,

            "issuer": self.issuer,

            "subject": self.subject,

            "serial_number": self.serial_number,

            "fingerprint_sha256":
                self.fingerprint_sha256,


            "valid_from":
                self.valid_from.isoformat()
                if self.valid_from else None,


            "valid_to":
                self.valid_to.isoformat()
                if self.valid_to else None,


            "risk_level":
                self.risk_level,


            "risk_score":
                self.risk_score,


            "policy_decision":
                self.policy_decision,


            "migration_required":
                self.migration_required,


            "recommended_algorithm":
                self.recommended_algorithm,


            "scan_status":
                self.scan_status,


            "scan_error":
                self.scan_error,


            "last_scanned":
                self.last_scanned.isoformat()
                if self.last_scanned else None,


            "created_at":
                self.created_at.isoformat()
                if self.created_at else None,


            "updated_at":
                self.updated_at.isoformat()
                if self.updated_at else None,
        }
