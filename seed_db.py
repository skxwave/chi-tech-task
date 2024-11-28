from werkzeug.security import generate_password_hash

from core.models import User, Article
from core import db
from app import create_app


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

    db.session.bulk_save_objects(users)
    db.session.bulk_save_objects(articles)
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_data()
