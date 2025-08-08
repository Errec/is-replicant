from fastapi.testclient import TestClient


def test_create_word_requires_token(client: TestClient) -> None:
    response = client.post(
        "/api/v1/admin/words",
        json={"word": "algorithm", "ai_likelihood": 0.2},
    )
    assert response.status_code == 401


def test_create_word_with_invalid_token(client: TestClient) -> None:
    headers = {"Authorization": "Bearer invalid"}
    response = client.post(
        "/api/v1/admin/words",
        json={"word": "test", "ai_likelihood": 0.3},
        headers=headers,
    )
    assert response.status_code == 403


def test_create_word_missing_field_returns_422(client: TestClient, auth_headers: dict) -> None:
    response = client.post(
        "/api/v1/admin/words",
        json={"word": "incomplete"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_create_and_get_word(client: TestClient, auth_headers: dict) -> None:
    payload = {"word": "algorithm", "ai_likelihood": 0.6}
    create_resp = client.post("/api/v1/admin/words", json=payload, headers=auth_headers)
    assert create_resp.status_code == 201
    word_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/v1/admin/words/{word_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["word"] == payload["word"]


def test_create_duplicate_word_returns_400(client: TestClient, auth_headers: dict) -> None:
    payload = {"word": "duplicate", "ai_likelihood": 0.4}
    first = client.post("/api/v1/admin/words", json=payload, headers=auth_headers)
    assert first.status_code == 201
    second = client.post("/api/v1/admin/words", json=payload, headers=auth_headers)
    assert second.status_code == 400
    assert second.json()["detail"] == "Word already exists"


def test_get_word_not_found(client: TestClient, auth_headers: dict) -> None:
    response = client.get("/api/v1/admin/words/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_word_success(client: TestClient, auth_headers: dict) -> None:
    payload = {"word": "update", "ai_likelihood": 0.2}
    create_resp = client.post("/api/v1/admin/words", json=payload, headers=auth_headers)
    word_id = create_resp.json()["id"]

    update_payload = {"word": "updated", "ai_likelihood": 0.8}
    update_resp = client.put(
        f"/api/v1/admin/words/{word_id}",
        json=update_payload,
        headers=auth_headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["word"] == "updated"


def test_update_word_not_found(client: TestClient, auth_headers: dict) -> None:
    payload = {"word": "missing", "ai_likelihood": 0.3}
    response = client.put(
        "/api/v1/admin/words/999",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_delete_word_success(client: TestClient, auth_headers: dict) -> None:
    payload = {"word": "remove", "ai_likelihood": 0.2}
    create_resp = client.post("/api/v1/admin/words", json=payload, headers=auth_headers)
    word_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/v1/admin/words/{word_id}", headers=auth_headers)
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/v1/admin/words/{word_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_delete_word_not_found(client: TestClient, auth_headers: dict) -> None:
    response = client.delete("/api/v1/admin/words/999", headers=auth_headers)
    assert response.status_code == 404
