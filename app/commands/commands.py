from flask import Blueprint
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.models import User
from core import db

bp = Blueprint("admin", __name__)


@bp.cli.command("create_user")
def create_user():
    username = input("Username: ")
    password = input("Password: ")
    role = input("Role: ")

    user = User(
        username=username,
        role=role,
    )
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        print("User created")
    except IntegrityError:
        print("User already exists")


@bp.cli.command("delete_user")
def delete_user():
    username = input("Username: ")

    user = db.session.scalar(select(User).where(User.username == username))

    if not user:
        print("User not exists")
        return
    
    db.session.delete(user)
    db.session.commit()
    print("user deleted")
    