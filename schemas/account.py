from marshmallow import Schema, fields

class AccountSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    account_type = fields.Str()
    account_number = fields.Str()
    balance = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()