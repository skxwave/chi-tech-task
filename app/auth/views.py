from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import select

from core import db
from core.models import User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def access_token():
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
    refresh_token = create_refresh_token(identity=username)
    return {"access_token": access_token, "refresh_token": refresh_token}, 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    username = get_jwt_identity()
    access_token = create_access_token(identity=username)
    return {"msg": access_token}, 200
