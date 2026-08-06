from marshmallow import Schema, fields


class MonitoringStatusSchema(Schema):

    status = fields.String()
    timestamp = fields.String()


class SystemHealthSchema(Schema):

    cpu_usage = fields.Float()
    memory_usage = fields.Float()
    disk_usage = fields.Float()
    timestamp = fields.String()
