import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

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
from app.db.session import SessionLocal, engine

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

@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture()
def admin_token() -> str:
    """Return a valid admin JWT token for authentication tests."""
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "sub": "admin",
        "is_admin": True,
    }
    return jwt.encode(payload, os.environ["SECRET_KEY"], algorithm="HS256")

@pytest.fixture()
def auth_headers(admin_token: str) -> dict:
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture(autouse=True)
def clean_db():
    db = SessionLocal()
    try:
        db.query(models.Phrase).delete()
        db.query(models.Word).delete()
        db.commit()
        yield
    finally:
        db.close()
