from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from sqlalchemy import select

from core import db
from core.models import User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if not username or not password:
        return {"msg": "Username and password required"}, 400

    user = db.session.scalar(select(User).where(User.username == username))

    if not user:
        return {"msg": "User doesn't exist"}, 404

    if not user.password or not user.check_password(password):
        return {"msg": "Bad username or password"}, 401

    access_token = create_access_token(identity=username)
    return {"msg": access_token}, 200
