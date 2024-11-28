from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select

from core.models import User
from core import db


def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            username = get_jwt_identity()
            user = db.session.scalar(select(User).where(User.username == username))
            if user and user.role in required_roles:
                return func(*args, **kwargs)
            return {"msg": "access denied"}, 403
        return wrapper
    return decorator