from fastapi.testclient import TestClient


def test_analyze_valid_text_returns_analysis(client: TestClient) -> None:
    response = client.post("/api/v1/analyze", json={"text": "This is a simple test."})
    assert response.status_code == 200
    data = response.json()
    assert "word_analysis" in data
    assert "phrase_analysis" in data
    assert "overall_ai_likelihood" in data


def test_analyze_empty_text_returns_400(client: TestClient) -> None:
    response = client.post("/api/v1/analyze", json={"text": " "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Text must not be empty"


def test_analyze_missing_text_field_returns_422(client: TestClient) -> None:
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 422
