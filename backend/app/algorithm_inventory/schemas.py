from marshmallow import Schema, fields


class AlgorithmSchema(Schema):

    id = fields.Int(dump_only=True)

    algorithm_name = fields.Str(required=True)

    category = fields.Str(required=True)

    version = fields.Str()

    key_size = fields.Str()

    allowed = fields.Bool()

    active = fields.Bool()

    risk_level = fields.Str()

    recommended_mode = fields.Str()

    description = fields.Str()
