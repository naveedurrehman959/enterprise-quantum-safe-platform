from datetime import datetime

from app.extensions import db


class Session(db.Model):

    __tablename__ = "sessions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    jwt_id = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    ip_address = db.Column(
        db.String(100)
    )

    user_agent = db.Column(
        db.String(255)
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Session {self.id}>"
