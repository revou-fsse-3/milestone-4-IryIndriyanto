from db import db
from flask_smorest import Blueprint
from models.transaction import TransactionModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas.transaction import TransactionSchema

blp = Blueprint(
    "transactions",
    "transactions",
    description="data of transactions",
    url_prefix="/transactions",
)


@blp.route("/")
@blp.response(200, TransactionSchema(many=True))
def get_transactions():
    return TransactionModel.query.all()
