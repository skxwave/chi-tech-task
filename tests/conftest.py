import pytest
from sqlalchemy import select
from flask_jwt_extended import create_access_token

from app import create_app
from core.models import Article, User, Base
from core.config import Config
from core import db


def create_user(username, role):
    data = {
        "username": username,
        "role": role,
    }
    user = User(**data)
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture(scope="package")
def app():
    config = Config()
    config.SQLALCHEMY_DATABASE_URI = "sqlite:///"
    config.TESTING = True

    app = create_app(config_class=config)
    return app


@pytest.fixture(scope="module")
def test_client(app):
    with app.app_context():
        with app.test_client() as client:
            Base.metadata.create_all(bind=db.engine)
            yield client
            Base.metadata.drop_all(bind=db.engine)


@pytest.fixture(scope="module")
def runner(app):
    with app.app_context():
        Base.metadata.create_all(bind=db.engine)
        yield app.test_cli_runner()
        Base.metadata.drop_all(bind=db.engine)


@pytest.fixture(scope="function")
def mock_user():
    user = create_user("user", "user")
    yield user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="function")
def mock_editor():
    user = create_user("editor", "editor")
    yield user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="function")
def mock_admin():
    user = create_user("admin", "admin")
    yield user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="function")
def access_token():
    def _access_token(username):
        return create_access_token(identity=username)
    return _access_token


@pytest.fixture(scope="function")
def mock_article(mock_user: User):
    data = {
        "title": "Test Article",
        "content": "Test Content",
        "user_id": mock_user.id,
    }
    article = Article(**data)
    db.session.add(article)
    db.session.commit()

    yield article

    if db.session.scalar(select(Article).where(Article.id == article.id)):
        db.session.delete(article)
        db.session.commit()
