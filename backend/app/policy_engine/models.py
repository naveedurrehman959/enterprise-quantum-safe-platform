from datetime import datetime
from app import db


class CryptoPolicy(db.Model):
    __tablename__ = "crypto_policies"

    id = db.Column(db.Integer, primary_key=True)

    algorithm_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    enabled = db.Column(
        db.Boolean,
        default=True
    )

    deployment_mode = db.Column(
        db.String(20),
        default="CLASSICAL"
    )
    # CLASSICAL
    # HYBRID
    # PURE_PQC

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "algorithm_name": self.algorithm_name,
            "enabled": self.enabled,
            "deployment_mode": self.deployment_mode
        }
