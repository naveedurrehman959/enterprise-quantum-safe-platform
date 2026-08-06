from datetime import datetime

from app.extensions import db


class AuditLog(db.Model):

    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=True
    )

    action = db.Column(
        db.String(100),
        nullable=False
    )

    module = db.Column(
        db.String(100),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<AuditLog {self.action}>"
    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "module": self.module,
            "status": self.status,
            "description": self.description,
            "timestamp": (
                self.timestamp.isoformat()
                if self.timestamp
                else None
            ),
        }
