from datetime import datetime

from app.extensions import db


class Compliance(db.Model):

    __tablename__ = "compliance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    control_name = db.Column(
        db.String(255),
        nullable=False
    )

    framework = db.Column(
        db.String(100),
        nullable=False
    )

    control_status = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    last_checked = db.Column(
        db.DateTime,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Compliance {self.control_name}>"
        )
