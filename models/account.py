from db import db


class AccountModel(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, nullable=False, dumb_only=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, dumb_only=True)
    account_type = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), unique=True, nullable=False, dumb_only=True)
    balance = db.Column(db.Float(10, 2), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=db.func.now(), nullable=False, dumb_only=True
    )
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now(), dumb_only=True)
