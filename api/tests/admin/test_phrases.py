from fastapi.testclient import TestClient


def test_create_phrase_requires_token(client: TestClient) -> None:
    response = client.post(
        "/api/v1/admin/phrases",
        json={"phrase": "hello world", "ai_likelihood": 0.2},
    )
    assert response.status_code == 401


def test_create_phrase_with_invalid_token(client: TestClient) -> None:
    headers = {"Authorization": "Bearer invalid"}
    response = client.post(
        "/api/v1/admin/phrases",
        json={"phrase": "hello", "ai_likelihood": 0.1},
        headers=headers,
    )
    assert response.status_code == 403


def test_create_phrase_missing_field_returns_422(client: TestClient, auth_headers: dict) -> None:
    response = client.post(
        "/api/v1/admin/phrases",
        json={"phrase": "incomplete"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_create_and_get_phrase(client: TestClient, auth_headers: dict) -> None:
    payload = {"phrase": "synthetic narrative", "ai_likelihood": 0.7}
    create_resp = client.post("/api/v1/admin/phrases", json=payload, headers=auth_headers)
    assert create_resp.status_code == 201
    phrase_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/v1/admin/phrases/{phrase_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["phrase"] == payload["phrase"]


def test_create_duplicate_phrase_returns_400(client: TestClient, auth_headers: dict) -> None:
    payload = {"phrase": "duplicate phrase", "ai_likelihood": 0.5}
    first = client.post("/api/v1/admin/phrases", json=payload, headers=auth_headers)
    assert first.status_code == 201
    second = client.post("/api/v1/admin/phrases", json=payload, headers=auth_headers)
    assert second.status_code == 400
    assert second.json()["detail"] == "Phrase already exists"


def test_get_phrase_not_found(client: TestClient, auth_headers: dict) -> None:
    response = client.get("/api/v1/admin/phrases/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_phrase_success(client: TestClient, auth_headers: dict) -> None:
    payload = {"phrase": "update me", "ai_likelihood": 0.1}
    create_resp = client.post("/api/v1/admin/phrases", json=payload, headers=auth_headers)
    phrase_id = create_resp.json()["id"]

    update_payload = {"phrase": "updated", "ai_likelihood": 0.9}
    update_resp = client.put(
        f"/api/v1/admin/phrases/{phrase_id}",
        json=update_payload,
        headers=auth_headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["phrase"] == "updated"


def test_update_phrase_not_found(client: TestClient, auth_headers: dict) -> None:
    payload = {"phrase": "missing", "ai_likelihood": 0.3}
    response = client.put(
        "/api/v1/admin/phrases/999",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_delete_phrase_success(client: TestClient, auth_headers: dict) -> None:
    payload = {"phrase": "remove me", "ai_likelihood": 0.2}
    create_resp = client.post("/api/v1/admin/phrases", json=payload, headers=auth_headers)
    phrase_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/v1/admin/phrases/{phrase_id}", headers=auth_headers)
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/v1/admin/phrases/{phrase_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_delete_phrase_not_found(client: TestClient, auth_headers: dict) -> None:
    response = client.delete("/api/v1/admin/phrases/999", headers=auth_headers)
    assert response.status_code == 404
