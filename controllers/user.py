from db import db
from flask import jsonify
from flask_smorest import Blueprint, abort
from models.user import UserModel
from schemas.user import UserRegistrationSchema
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256

blp = Blueprint("users", "users", description="data of users")


@blp.route("/users", methods=["GET"])
def get_users():
    return "this is list of users"


@blp.route("/register", methods=["POST"])
@blp.arguments(UserRegistrationSchema)
@blp.response(200)
def create_user(user_data):
    user = UserModel(
        username=user_data["username"],
        email=user_data["email"],
        password_hash=pbkdf2_sha256.hash(user_data["password"]),
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({"Error": "Username or email already exists."}), 400
