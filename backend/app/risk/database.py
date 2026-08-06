from app import db


class AlgorithmRisk(db.Model):

    __tablename__ = "algorithm_risk"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    algorithm = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    quantum_vulnerable = db.Column(
        db.Boolean,
        default=False
    )

    risk_level = db.Column(
        db.String(20)
    )

    risk_score = db.Column(
        db.Integer
    )

    recommendation = db.Column(
        db.String(100)
    )

    migration_required = db.Column(
        db.Boolean,
        default=False
    )
