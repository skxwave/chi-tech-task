from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..helpers import role_required
from core import db
from core.models import User

bp = Blueprint("users", __name__)


@bp.route("", methods=["GET"])
# @jwt_required()
def get_all_users():
    page = request.args.get('page', 1, type=int)

    if page <= 0:
        return {"msg": "page should be > 0"}

    query = db.session.query(User)
    total_items = query.count()
    per_page = current_app.config["PAGE_SIZE"]
    users = query.offset((page - 1) * per_page).limit(per_page).all()
    return {
        "page": page,
        "total_items": total_items,
        "data": [user.to_dict() for user in users]
    }, 200


@bp.route("/search", methods=["GET"])
@jwt_required()
def search_users():
    query = request.args.get("q", "")
    users = db.session.scalars(select(User).filter(User.username.ilike(f"%{query}%")))

    return {"msg": [user.to_dict() for user in users]}, 200


@bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def find_user(user_id):
    user = db.session.scalar(select(User).where(User.id == user_id))

    if not user:
        return {"msg": "user not found"}, 404

    return {"msg": user.to_dict()}


@bp.route("", methods=["POST"])
@jwt_required()
@role_required(["admin"])
def create_user():
    data = request.get_json()
    user = User(
        username=data["username"],
        role=data["role"],
    )
    user.set_password(data["password"])

    try:
        db.session.add(user)
        db.session.commit()
        return {"msg": "user created"}, 201
    except IntegrityError:
        return {"msg": "user already exists"}, 409


@bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@role_required(["admin"])
def update_user(user_id):
    data = request.get_json()
    user = db.session.scalar(select(User).where(User.id == user_id))

    if not user:
        return {"msg": "user not found"}, 404

    if not data:
        return {"msg": "fields missing"}, 400

    if "username" in data:
        user.username = data["username"]

    if "role" in data:
        user.role = data["role"]

    if "password" in data:
        user.set_password(data["password"])

    db.session.commit()

    return {"msg": "user updated"}, 200


@bp.route("<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_required(["admin"])
def delete_user(user_id):
    user = db.session.scalar(select(User).where(User.id == user_id))

    if not user:
        return {"msg": "user not found"}, 404

    db.session.delete(user)
    db.session.commit()

    return {"msg": "user deleted"}, 200
