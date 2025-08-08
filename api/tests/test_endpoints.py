import os
from datetime import datetime, timedelta

import sys
from pathlib import Path

import nltk
import pytest
from fastapi.testclient import TestClient
from jose import jwt

# Ensure the application package is importable
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Configure environment for testing before importing the app
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "testsecret")

# Ensure required NLTK data is available
nltk.download("punkt", quiet=True)
try:  # pragma: no cover - defensive download for newer NLTK versions
    nltk.download("punkt_tab", quiet=True)
except Exception:  # pragma: no cover - ignore if dataset missing
    pass

from app.main import app
from app.api.dependencies import get_db
from app.db import models
from app.db.session import engine, SessionLocal

# Create the database tables for tests
models.Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the testing session

def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def admin_token() -> str:
    """Return a valid admin JWT token for authentication tests."""
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "sub": "admin",
        "is_admin": True,
    }
    return jwt.encode(payload, os.environ["SECRET_KEY"], algorithm="HS256")


def test_analyze_valid_text_returns_analysis():
    response = client.post("/api/v1/analyze", json={"text": "This is a simple test."})
    assert response.status_code == 200
    data = response.json()
    assert "word_analysis" in data
    assert "phrase_analysis" in data
    assert "overall_ai_likelihood" in data


def test_analyze_empty_text_returns_400():
    response = client.post("/api/v1/analyze", json={"text": " "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Text must not be empty"


def test_admin_create_phrase_requires_token():
    response = client.post(
        "/api/v1/admin/phrases",
        json={"phrase": "hello world", "ai_likelihood": 0.2},
    )
    assert response.status_code == 401


def test_admin_create_and_get_phrase(admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"phrase": "synthetic narrative", "ai_likelihood": 0.7}
    create_resp = client.post("/api/v1/admin/phrases", json=payload, headers=headers)
    assert create_resp.status_code == 201
    phrase_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/v1/admin/phrases/{phrase_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["phrase"] == payload["phrase"]


def test_admin_create_and_get_word(admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"word": "algorithm", "ai_likelihood": 0.6}
    create_resp = client.post("/api/v1/admin/words", json=payload, headers=headers)
    assert create_resp.status_code == 201
    word_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/v1/admin/words/{word_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["word"] == payload["word"]
