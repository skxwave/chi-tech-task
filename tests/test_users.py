from core.models import User


def test_get_all_users(test_client, access_token):
    response = test_client.get("/api/v1/users", headers={"Authorization": f"Bearer {access_token("user")}"})

    assert response.status_code == 200
    assert isinstance(response.json["msg"], list)


def test_get_one_user(test_client, mock_user, access_token):
    response = test_client.get(f"/api/v1/users/{mock_user.id}", headers={"Authorization": f"Bearer {access_token("user")}"})

    assert response.status_code == 200
    assert response.json["msg"]["username"] == "user"


def test_search_user(test_client, mock_user, access_token):
    response = test_client.get("/api/v1/users/search?q=user", headers={"Authorization": f"Bearer {access_token("user")}"})

    assert response.status_code == 200
    assert response.json["msg"][0]["username"] == "user"


def test_create_user(test_client, mock_admin, access_token):
    data = {
        "username": "TestUser",
        "password": "123454",
        "role": "user",
    }
    response = test_client.post("/api/v1/users", headers={"Authorization": f"Bearer {access_token("admin")}"}, json=data)

    assert response.status_code == 201
    assert response.json["msg"] == "user created"


def test_update_user(test_client, mock_user, mock_admin, access_token):
    data = {
        "username": "UpdatedUser",
        "password": "123456",
        "role": "user",
    }
    response = test_client.put(f"/api/v1/users/{mock_user.id}", headers={"Authorization": f"Bearer {access_token("admin")}"}, json=data)

    assert response.status_code == 200
    assert response.json["msg"] == "user updated"


def test_delete_user(test_client, mock_user, mock_admin, access_token):
    response = test_client.delete(f"/api/v1/users/{mock_user.id}", headers={"Authorization": f"Bearer {access_token("admin")}"})

    assert response.status_code == 200
    assert response.json["msg"] == "user deleted"
