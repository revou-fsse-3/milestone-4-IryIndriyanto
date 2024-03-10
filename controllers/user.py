from flask_smorest import Blueprint
from models.user import UserModel
from schemas.user import UserSchema

from db import db

blp = Blueprint("users", "users", description="data of users", url_prefix="/users")

@blp.route("/")
def get_users():
    return "this is list of users"