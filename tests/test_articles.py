from core.models import User, Article


def test_get_one_article(test_client, mock_user, access_token, mock_article):
    response = test_client.get(f"/api/v1/articles/{mock_article.id}", headers={"Authorization": f"Bearer {access_token("user")}"})
    data = response.json["msg"]

    assert response.status_code == 200
    assert data["title"] == "Test Article"
    assert data["content"] == "Test Content"


def test_get_articles(test_client, mock_user, access_token):
    response = test_client.get(f"/api/v1/articles", headers={"Authorization": f"Bearer {access_token("user")}"})

    assert response.status_code == 200
    assert isinstance(response.json["msg"], list)


def test_create_article(test_client, mock_user, access_token):
    article = {
        "title": "Created article",
        "content": "Created content",
    }
    response = test_client.post(f"/api/v1/articles", json=article, headers={"Authorization": f"Bearer {access_token("user")}"})
    data = response.json["msg"]

    assert response.status_code == 201
    assert data["title"] == "Created article"
    assert data["content"] == "Created content"


def test_update_article(test_client, mock_user, mock_article, access_token):
    article = {
        "title": "Updated article",
        "content": "Updated content",
    }
    response = test_client.put(f"/api/v1/articles/{mock_article.id}", json=article, headers={"Authorization": f"Bearer {access_token("user")}"})
    data = response.json["result"]

    assert response.status_code == 200
    assert data["title"] == "Updated article"
    assert data["content"] == "Updated content"


def test_search_article(test_client, access_token, mock_article):
    response = test_client.get(f"/api/v1/articles/search?q=Test", headers={"Authorization": f"Bearer {access_token("user")}"})

    assert response.status_code == 200
    assert response.json["msg"][0]["title"] == "Test Article"


def test_delete_article(test_client, mock_user, mock_article, access_token):
    response = test_client.delete(f"/api/v1/articles/{mock_article.id}", headers={"Authorization": f"Bearer {access_token("user")}"})
    
    assert response.status_code == 200
