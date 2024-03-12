from marshmallow import Schema, fields

class AccountSchema(Schema):
    account_type = fields.Str()