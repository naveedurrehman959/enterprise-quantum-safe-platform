from datetime import datetime

from app.extensions import db


class Certificate(db.Model):

    __tablename__ = "certificates"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        nullable=False
    )


    certificate_serial_number = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )


    certificate_type = db.Column(
        db.String(100),
        nullable=False
    )


    certificate_reference = db.Column(
        db.String(255),
        nullable=False
    )


    # Cryptographic Information

    algorithm = db.Column(
        db.String(100),
        nullable=False,
        default="ML-DSA-65"
    )


    algorithm_category = db.Column(
        db.String(100),
        default="DIGITAL_SIGNATURE"
    )


    risk_level = db.Column(
        db.String(50),
        default="SAFE"
    )


    migration_status = db.Column(
        db.String(100),
        default="COMPLETED"
    )


    recommended_algorithm = db.Column(
        db.String(255),
        default="ML-DSA-65"
    )


    certificate_status = db.Column(
        db.String(50),
        default="active"
    )


    issued_at = db.Column(
        db.DateTime,
        nullable=False
    )


    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    def to_dict(self):

        return {

            "id": self.id,

            "serial":
            self.certificate_serial_number,

            "type":
            self.certificate_type,

            "algorithm":
            self.algorithm,

            "algorithm_category":
            self.algorithm_category,

            "risk_level":
            self.risk_level,

            "migration_status":
            self.migration_status,

            "recommended_algorithm":
            self.recommended_algorithm,

            "status":
            self.certificate_status,

            "issued_at":
            self.issued_at.isoformat(),

            "expires_at":
            self.expires_at.isoformat()

        }


    def __repr__(self):

        return (
            f"<Certificate {self.certificate_serial_number}>"
        )
