from marshmallow import Schema, fields

class TransactionSchema(Schema):
    from_account_id = fields.Int()
    to_account_id = fields.Int()
    amount = fields.Decimal()
    type = fields.Str()
    description = fields.Str()