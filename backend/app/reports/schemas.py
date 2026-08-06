from marshmallow import Schema, fields


class ReportSchema(Schema):

    generated_at = fields.String()

    dashboard = fields.Dict()

    inventory = fields.Dict()

    risk = fields.Dict()

    compliance = fields.Dict()

    monitoring = fields.Dict()
