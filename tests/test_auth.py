from flask.testing import FlaskClient

from core.models import User


def test_login(test_client: FlaskClient, mock_user: User):
    data = {
        "username": "user",
        "password": "password",
    }
    response = test_client.post("/api/v1/auth/login", json=data)

    assert response.status_code == 200