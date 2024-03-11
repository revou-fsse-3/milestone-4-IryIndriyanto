from marshmallow import Schema, fields

class TransactionSchema(Schema):
    id = fields.Int()
    from_account_id = fields.Int()
    to_account_id = fields.Int()
    balance = fields.Float()
    type = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
