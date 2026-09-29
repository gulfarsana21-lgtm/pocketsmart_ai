import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"

        from app import config
        config.settings.DATABASE_PATH = str(db_path)
        config.settings.SECRET_KEY = "test-secret-key"
        config.settings.GEMINI_API_KEY = ""

        from app.database import init_db
        init_db()

        from app.main import app
        with TestClient(app) as test_client:
            yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_login_and_session(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123456",
        },
    )
    assert response.status_code == 200

    response = client.get("/api/session-info")
    assert response.status_code == 200
    assert response.json()["logged_in"] is True

    response = client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "test@example.com"


def test_home_fallback_and_history(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Planner User",
            "email": "planner@example.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/api/planners/home",
        json={
            "budget": 50000,
            "rooms": ["Living Room", "Bedroom"],
            "style": "Modern",
            "city": "Coimbatore",
            "notes": "Affordable furniture",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["planner"] == "home"
    assert data["history_id"] is not None
    assert data["ai_generated"] is False
    assert len(data["recommendations"]) >= 1

    history = client.get("/api/history")
    assert history.status_code == 200
    assert len(history.json()) == 1

    detail = client.get(
        f"/api/recommendations-details/{data['history_id']}"
    )
    assert detail.status_code == 200


def test_party_fallback(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Party User",
            "email": "party@example.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/api/planners/party",
        json={
            "budget": 30000,
            "guests": 50,
            "event_type": "Birthday",
            "venue": "Function Hall",
            "city": "Coimbatore",
            "notes": "Vegetarian food",
        },
    )

    assert response.status_code == 200
    assert response.json()["planner"] == "party"
