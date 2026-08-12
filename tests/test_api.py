from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"
    assert data["docs"] == "/docs"


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert "application" in data
    assert "version" in data
    assert "timestamp" in data
