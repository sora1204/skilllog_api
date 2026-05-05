def test_create_category(client, auth_headers):
    response = client.post(
        "/categories",
        headers=auth_headers,
        json={
            "name": "FastAPI",
            "description": "FastAPIとAPI開発の学習",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "FastAPI"
    assert data["description"] == "FastAPIとAPI開発の学習"
    assert data["owner_id"] == 1


def test_get_categories(client, auth_headers):
    client.post(
        "/categories",
        headers=auth_headers,
        json={
            "name": "FastAPI",
            "description": "FastAPIとAPI開発の学習",
        },
    )

    response = client.get(
        "/categories",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "FastAPI"


def test_create_duplicate_category(client, auth_headers):
    category_data = {
        "name": "FastAPI",
        "description": "FastAPIとAPI開発の学習",
    }

    client.post(
        "/categories",
        headers=auth_headers,
        json=category_data,
    )

    response = client.post(
        "/categories",
        headers=auth_headers,
        json=category_data,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Category name already exists"


def test_category_requires_auth(client):
    response = client.get("/categories")

    assert response.status_code == 401


def test_other_user_cannot_access_category(client, auth_headers, other_auth_headers):
    create_response = client.post(
        "/categories",
        headers=auth_headers,
        json={
            "name": "FastAPI",
            "description": "FastAPIとAPI開発の学習",
        },
    )

    category_id = create_response.json()["id"]

    response = client.get(
        f"/categories/{category_id}",
        headers=other_auth_headers,
    )

    assert response.status_code == 404