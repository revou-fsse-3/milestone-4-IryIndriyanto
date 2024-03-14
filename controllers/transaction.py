from db import db
from flask import jsonify
from flask_smorest import Blueprint
from models.transaction import TransactionModel
from models.account import AccountModel
from sqlalchemy.exc import SQLAlchemyError
from schemas.transaction import TransactionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

blp = Blueprint(
    "transactions",
    "transactions",
    description="data of transactions",
    url_prefix="/transactions",
)


@blp.route("/", methods=["GET"])
@jwt_required()
@blp.response(200, TransactionSchema(many=True))
def get_transactions():
    user_id = get_jwt_identity()
    account_ids = (
        AccountModel.query.with_entities(AccountModel.id)
        .filter_by(user_id=user_id)
        .all()
    )
    if account_ids:
        account_ids_list = [account[0] for account in account_ids]
        transaction_list = []
        for account_id in account_ids_list:
            transactions = TransactionModel.query.filter(
                (TransactionModel.to_account_id == account_id)
                | (TransactionModel.from_account_id == account_id)
            ).all()
            transaction_list.extend(transactions)
        return transaction_list
    return jsonify({"message": "Transaction not found"}), 404


@blp.route("/<int:transaction_id>", methods=["GET"])
@jwt_required()
@blp.response(200, TransactionSchema)
def get_transaction(transaction_id):
    user_id = get_jwt_identity()
    account_ids = (
        AccountModel.query.with_entities(AccountModel.id)
        .filter_by(user_id=user_id)
        .all()
    )
    account_ids_list = [account[0] for account in account_ids]
    transaction = db.session.get(TransactionModel, transaction_id)
    if transaction is None:
        return jsonify({"message": "Transaction not found"}), 404
    if transaction and (
        transaction.from_account_id in account_ids_list
        or transaction.to_account_id in account_ids_list
    ):
        return transaction
    else:
        return jsonify({"message": "You are not authorized"}), 403


@blp.route("/", methods=["POST"])
@blp.arguments(TransactionSchema)
@jwt_required()
@blp.response(200)
def create_new_transaction(transaction_data):
    try:
        user_id = get_jwt_identity()

        if transaction_data["type"] == "deposit":
            to_account = AccountModel.query.filter_by(
                id=transaction_data["to_account_id"], user_id=user_id
            ).first()
            new_transaction = TransactionModel(
                from_account_id=None,
                to_account_id=transaction_data["to_account_id"],
                amount=transaction_data["amount"],
                type="deposit",
                description=transaction_data["description"],
            )
            to_account.balance += transaction_data["amount"]
            db.session.add(new_transaction)
            db.session.commit()
            return jsonify({"message": "Deposit successful."}), 200

        elif transaction_data["type"] == "transfer":
            from_account = AccountModel.query.filter_by(
                id=transaction_data["from_account_id"], user_id=user_id
            ).first()
            to_account = AccountModel.query.filter_by(
                id=transaction_data["to_account_id"], user_id=user_id
            ).first()

            if from_account.balance < transaction_data["amount"]:
                return jsonify({"Error": "Insufficient balance."}), 400
            new_transaction = TransactionModel(
                from_account_id=transaction_data["from_account_id"],
                to_account_id=transaction_data["to_account_id"],
                amount=transaction_data["amount"],
                type="transfer",
                description=transaction_data["description"],
            )
            to_account.balance += transaction_data["amount"]
            from_account.balance -= transaction_data["amount"]
            db.session.add(new_transaction)
            db.session.commit()
            return jsonify({"message": "Transfer successful."}), 200

        elif transaction_data["type"] == "withdrawal":
            from_account = AccountModel.query.filter_by(
                id=transaction_data["from_account_id"], user_id=user_id
            ).first()

            if from_account.balance < transaction_data["amount"]:
                return jsonify({"Error": "Insufficient balance."}), 400
            new_transaction = TransactionModel(
                from_account_id=transaction_data["from_account_id"],
                to_account_id=None,
                amount=transaction_data["amount"],
                type="withdrawal",
                description=transaction_data["description"],
            )
            from_account.balance -= transaction_data["amount"]
            db.session.add(new_transaction)
            db.session.commit()
            return jsonify({"message": "Withdrawal successful."}), 200
        else:
            return jsonify({"Error": "Invalid transaction type."}), 400

    except SQLAlchemyError:
        return jsonify({"Error": "internal server error."}), 500
