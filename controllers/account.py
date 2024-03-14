import random
from db import db
from flask import jsonify
from flask_smorest import Blueprint
from models.account import AccountModel
from sqlalchemy.exc import IntegrityError
from schemas.account import AccountSchema, CompleteAccountSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

blp = Blueprint(
    "accounts", "accounts", description="data of accounts", url_prefix="/accounts"
)


@blp.route("/", methods=["GET"])
@jwt_required()
@blp.response(200, CompleteAccountSchema(many=True))
def get_accounts():
    user_id = get_jwt_identity()
    accounts = AccountModel.query.filter_by(user_id=user_id)
    if accounts:
        return accounts
    return jsonify({"message": "Account not found"}), 404


@blp.route("/<int:account_id>", methods=["GET"])
@jwt_required()
@blp.response(200, CompleteAccountSchema)
def get_account(account_id):
    user_id = get_jwt_identity()
    account = db.session.get(AccountModel, account_id)
    if account.user_id != user_id:
        return jsonify({"message": "You are not authorized"}), 403
    if account:
        return account
    return jsonify({"message": "Account not found"}), 404


@blp.route("/", methods=["POST"])
@blp.arguments(AccountSchema)
@jwt_required()
@blp.response(200)
def create_new_account(account_data):
    try:
        new_account = AccountModel(
            user_id=get_jwt_identity(),
            account_type=account_data["account_type"],
            account_number="".join(str(random.randint(0, 9)) for _ in range(10)),
            balance=0,
        )
        db.session.add(new_account)
        db.session.commit()
    except IntegrityError:
        return jsonify({"Error": "account number already exists."}), 400


@blp.route("/<int:account_id>", methods=["PUT"])
@blp.arguments(AccountSchema)
@jwt_required()
@blp.response(200)
def edit_user_profile(updated_account_data, account_id):
    user_id = get_jwt_identity()
    account = db.session.get(AccountModel, account_id)
    if account.user_id != user_id:
        return jsonify({"message": "You are not authorized"}), 403
    if account:
        AccountModel.query.filter_by(id=account_id, user_id=user_id).update(updated_account_data)
        db.session.commit()
        return jsonify({"message": "Account updated"}), 200
    return jsonify({"message": "Account not found"}), 404


@blp.route("/<int:account_id>", methods=["DELETE"])
@jwt_required()
@blp.response(200)
def edit_user_profile(account_id):
    user_id = get_jwt_identity()
    account = db.session.get(AccountModel, account_id)
    if account.user_id != user_id:
        return jsonify({"message": "You are not authorized"}), 403
    if account:
        db.session.delete(account)
        db.session.commit()
        return jsonify({"message": "Account deleted"}), 200
    return jsonify({"message": "Account not found"}), 404
