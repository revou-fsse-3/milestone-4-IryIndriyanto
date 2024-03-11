from db import db


class TransactionModel(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    from_account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    balance = db.Column(db.Float(10, 2), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
