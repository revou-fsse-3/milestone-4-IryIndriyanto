from db import db
from flask import jsonify
from flask_smorest import Blueprint
from models.user import UserModel
from schemas.user import UserSchema
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token

blp = Blueprint("users", "users", description="data of users", url_prefix="/users")


@blp.route("/", methods=["POST"])
@blp.arguments(UserSchema)
@blp.response(200)
def user_register(user_data):
    new_user = UserModel(
        username=user_data["username"],
        email=user_data["email"],
        password_hash=pbkdf2_sha256.hash(user_data["password"]),
    )
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        return jsonify({"Error": "Username or email already exists."}), 400


@blp.route("/login", methods=["POST"])
@blp.arguments(UserSchema)
@blp.response(200)
def user_login(user_data):
    user = UserModel.query.filter_by(username=user_data["username"]).first()
    if user and pbkdf2_sha256.verify(user_data["password"], user.password_hash):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return (
            jsonify({"access token": access_token, "refresh token": refresh_token}),
            200,
        )
    return jsonify({"message": "Invalid credentials"}), 401
