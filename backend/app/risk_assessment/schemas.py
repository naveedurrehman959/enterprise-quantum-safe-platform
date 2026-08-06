# backend/app/risk_assessment/schemas.py

from marshmallow import (
    Schema,
    fields,
    validate,
)


class RiskAssessmentSchema(Schema):

    algorithm = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=50,
        ),
    )
