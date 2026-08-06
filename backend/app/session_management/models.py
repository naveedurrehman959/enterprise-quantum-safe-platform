from datetime import datetime

from app import db


class UserSession(db.Model):

    __tablename__ = "user_sessions"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        nullable=False
    )


    jwt_jti = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )


    ip_address = db.Column(
        db.String(100),
        nullable=True
    )


    device_info = db.Column(
        db.String(255),
        nullable=True
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    last_activity = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )


    status = db.Column(
        db.String(50),
        default="active"
    )


    def to_dict(self):

        return {

            "id": self.id,

            "user_id": self.user_id,

            "jwt_jti": self.jwt_jti,

            "ip_address": self.ip_address,

            "device_info": self.device_info,

            "created_at": self.created_at.isoformat(),

            "last_activity": self.last_activity.isoformat(),

            "expires_at": self.expires_at.isoformat(),

            "status": self.status

        }
