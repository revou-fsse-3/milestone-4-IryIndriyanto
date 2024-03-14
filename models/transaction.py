from db import db
from enum import Enum

class TransactionType(Enum):
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'
    DEPOSIT = 'deposit'

class TransactionModel(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    from_account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    to_account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), nullable=False)