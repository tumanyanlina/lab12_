import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "app_name" in response.json()
    assert "version" in response.json()
    assert "endpoints" in response.json()