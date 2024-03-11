from db import db
from flask_smorest import Blueprint
from models.account import AccountModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas.account import AccountSchema

blp = Blueprint(
    "accounts", "accounts", description="data of accounts", url_prefix="/accounts"
)


@blp.route("/")
@blp.response(200, AccountSchema(many=True))
def get_accounts():
    return AccountModel.query.all()