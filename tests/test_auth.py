def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "tsubasa",
            "email": "tsubasa@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "tsubasa"
    assert data["email"] == "tsubasa@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    user_data = {
        "username": "tsubasa",
        "email": "tsubasa@example.com",
        "password": "password123",
    }

    client.post("/auth/register", json=user_data)

    response = client.post(
        "/auth/register",
        json={
            "username": "another",
            "email": "tsubasa@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "username": "tsubasa",
            "email": "tsubasa@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "tsubasa@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "username": "tsubasa",
            "email": "tsubasa@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "tsubasa@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_users_me_requires_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_users_me_with_token(client, auth_headers):
    response = client.get(
        "/users/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "tsubasa"
    assert data["email"] == "tsubasa@example.com"