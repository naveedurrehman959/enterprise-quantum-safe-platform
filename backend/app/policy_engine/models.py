from datetime import datetime

from app import db


class CryptoPolicy(db.Model):

    __tablename__ = "crypto_policies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    algorithm_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    enabled = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    deployment_mode = db.Column(
        db.String(20),
        default="CLASSICAL",
        nullable=False
    )

    enforcement_action = db.Column(
        db.String(30),
        default="ALLOW",
        nullable=False
    )

    priority = db.Column(
        db.Integer,
        default=100,
        nullable=False
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

            "algorithm_name":
                self.algorithm_name,

            "enabled":
                self.enabled,

            "deployment_mode":
                self.deployment_mode,

            "enforcement_action":
                self.enforcement_action,

            "priority":
                self.priority,

            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),

            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            )
        }
