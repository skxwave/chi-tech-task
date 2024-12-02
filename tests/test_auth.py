from flask_jwt_extended import create_refresh_token
from flask.testing import FlaskClient

from core.models import User


def test_login(test_client: FlaskClient, mock_user: User):
    data = {
        "username": "user",
        "password": "password",
    }
    response = test_client.post("/api/v1/auth/login", json=data)

    assert response.status_code == 200


def test_refresh_token(test_client: FlaskClient):
    token = create_refresh_token(identity="user")
    response = test_client.post("/api/v1/auth/refresh", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
