from datetime import datetime

from app.extensions import db


class CryptoKeys(db.Model):

    __tablename__ = "crypto_keys"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    algorithm = db.Column(
        db.String(100),
        nullable=False
    )

    public_key = db.Column(
        db.Text,
        nullable=False
    )

    private_key_reference = db.Column(
        db.String(255),
        nullable=False
    )

    key_version = db.Column(
        db.Integer,
        default=1
    )

    key_status = db.Column(
        db.String(50),
        default="active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    expires_at = db.Column(
        db.DateTime
    )

    def __repr__(self):
        return (
            f"<CryptoKey {self.algorithm}>"
        )
