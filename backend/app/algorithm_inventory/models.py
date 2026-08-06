from datetime import datetime
from app import db


class AlgorithmAsset(db.Model):

    __tablename__ = "algorithm_assets"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    algorithm_name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    version = db.Column(
        db.String(50)
    )

    key_size = db.Column(
        db.String(50)
    )

    allowed = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    deployment_mode = db.Column(
        db.String(20),
        default="CLASSICAL",
        nullable=False
    )
    risk_level = db.Column(
        db.String(20),
        nullable=False
    )

    recommended_mode = db.Column(
        db.String(30),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "algorithm_name": self.algorithm_name,
            "category": self.category,
            "version": self.version,
            "key_size": self.key_size,
            "allowed": self.allowed,
            "active": self.active,
            "deployment_mode": self.deployment_mode,
            "risk_level": self.risk_level,
            "recommended_mode": self.recommended_mode,
            "description": self.description,
        }
    
