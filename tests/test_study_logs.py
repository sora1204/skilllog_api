def create_category(client, auth_headers):
    response = client.post(
        "/categories",
        headers=auth_headers,
        json={
            "name": "FastAPI",
            "description": "FastAPIとAPI開発の学習",
        },
    )

    return response.json()["id"]


def test_create_study_log(client, auth_headers):
    category_id = create_category(client, auth_headers)

    response = client.post(
        "/study-logs",
        headers=auth_headers,
        json={
            "study_date": "2026-05-04",
            "title": "FastAPIの認証APIを学習",
            "category_id": category_id,
            "minutes": 120,
            "resource": "FastAPI公式ドキュメント",
            "resource_url": "https://fastapi.tiangolo.com/",
            "note": "JWT認証とDependsの流れを確認した",
            "reflection": "ログイン中ユーザーを取得する流れが理解できた",
            "understanding_level": 4,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "FastAPIの認証APIを学習"
    assert data["minutes"] == 120
    assert data["category_id"] == category_id
    assert data["owner_id"] == 1


def test_get_study_logs(client, auth_headers):
    category_id = create_category(client, auth_headers)

    client.post(
        "/study-logs",
        headers=auth_headers,
        json={
            "study_date": "2026-05-04",
            "title": "FastAPIの認証APIを学習",
            "category_id": category_id,
            "minutes": 120,
            "resource": "FastAPI公式ドキュメント",
            "resource_url": "https://fastapi.tiangolo.com/",
            "note": "JWT認証とDependsの流れを確認した",
            "reflection": "ログイン中ユーザーを取得する流れが理解できた",
            "understanding_level": 4,
        },
    )

    response = client.get(
        "/study-logs",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "FastAPIの認証APIを学習"


def test_create_study_log_with_invalid_category(client, auth_headers):
    response = client.post(
        "/study-logs",
        headers=auth_headers,
        json={
            "study_date": "2026-05-04",
            "title": "存在しないカテゴリを指定",
            "category_id": 999,
            "minutes": 60,
            "resource": None,
            "resource_url": None,
            "note": None,
            "reflection": None,
            "understanding_level": 3,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Category not found"


def test_update_study_log(client, auth_headers):
    category_id = create_category(client, auth_headers)

    create_response = client.post(
        "/study-logs",
        headers=auth_headers,
        json={
            "study_date": "2026-05-04",
            "title": "FastAPIの認証APIを学習",
            "category_id": category_id,
            "minutes": 120,
            "resource": "FastAPI公式ドキュメント",
            "resource_url": "https://fastapi.tiangolo.com/",
            "note": "JWT認証とDependsの流れを確認した",
            "reflection": "少し理解できた",
            "understanding_level": 3,
        },
    )

    log_id = create_response.json()["id"]

    response = client.patch(
        f"/study-logs/{log_id}",
        headers=auth_headers,
        json={
            "minutes": 150,
            "reflection": "JWT認証の流れをかなり理解できた",
            "understanding_level": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["minutes"] == 150
    assert data["reflection"] == "JWT認証の流れをかなり理解できた"
    assert data["understanding_level"] == 5
    assert data["title"] == "FastAPIの認証APIを学習"


def test_delete_study_log(client, auth_headers):
    category_id = create_category(client, auth_headers)

    create_response = client.post(
        "/study-logs",
        headers=auth_headers,
        json={
            "study_date": "2026-05-04",
            "title": "削除テスト",
            "category_id": category_id,
            "minutes": 30,
            "resource": None,
            "resource_url": None,
            "note": None,
            "reflection": None,
            "understanding_level": 3,
        },
    )

    log_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/study-logs/{log_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Study log deleted"

    get_response = client.get(
        f"/study-logs/{log_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_other_user_cannot_access_study_log(client, auth_headers, other_auth_headers):
    category_id = create_category(client, auth_headers)

    create_response = client.post(
        "/study-logs",
        headers=auth_headers,
        json={
            "study_date": "2026-05-04",
            "title": "他人に見えないログ",
            "category_id": category_id,
            "minutes": 90,
            "resource": None,
            "resource_url": None,
            "note": None,
            "reflection": None,
            "understanding_level": 4,
        },
    )

    log_id = create_response.json()["id"]

    response = client.get(
        f"/study-logs/{log_id}",
        headers=other_auth_headers,
    )

    assert response.status_code == 404


def test_total_stats(client, auth_headers):
    category_id = create_category(client, auth_headers)

    client.post(
        "/study-logs",
        headers=auth_headers,
        json={
            "study_date": "2026-05-04",
            "title": "FastAPI",
            "category_id": category_id,
            "minutes": 120,
            "resource": None,
            "resource_url": None,
            "note": None,
            "reflection": None,
            "understanding_level": 4,
        },
    )

    client.post(
        "/study-logs",
        headers=auth_headers,
        json={
            "study_date": "2026-05-05",
            "title": "Docker",
            "category_id": category_id,
            "minutes": 60,
            "resource": None,
            "resource_url": None,
            "note": None,
            "reflection": None,
            "understanding_level": 4,
        },
    )

    response = client.get(
        "/stats/total",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_minutes"] == 180
    assert data["total_hours"] == 3.0
    assert data["log_count"] == 2