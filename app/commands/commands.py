import click
from flask import Blueprint
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from core.models import User, Article
from core import db

bp = Blueprint("admin", __name__)


@bp.cli.command("create_user")
@click.option("--username", required=True)
@click.option("--password", required=True)
@click.option("--role", required=True)
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
    

@bp.cli.command("seed_db")
def seed_data():
    users = [
        User(username="admin", password=generate_password_hash("admin"), role="admin"),
        User(username="editor", password=generate_password_hash("editor123"), role="editor"),
        User(username="user1", password=generate_password_hash("user123"), role="user"),
    ]

    articles = [
        Article(title="Article 1", content="This is the first article", user_id=3),
        Article(title="Article 2", content="This is the second article", user_id=3),
        Article(title="Editorial Review", content="Reviewed by editor", user_id=2),
    ]

    try:
        db.session.bulk_save_objects(users)
        db.session.bulk_save_objects(articles)
        db.session.commit()
        print("Database seeded successfully!")
    except IntegrityError:
        db.session.rollback()
        print("Sample data already exists, skipping...")