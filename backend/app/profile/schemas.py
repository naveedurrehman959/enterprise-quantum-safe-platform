from marshmallow import Schema, fields



class ProfileSchema(Schema):

    id = fields.Integer()

    username = fields.String()

    email = fields.Email()

    role = fields.String()

    created_at = fields.DateTime()



class UpdateProfileSchema(Schema):

    email = fields.Email()



class PasswordSchema(Schema):

    old_password = fields.String(
        required=True
    )

    new_password = fields.String(
        required=True
    )
