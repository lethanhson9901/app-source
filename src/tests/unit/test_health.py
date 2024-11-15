# src/tests/unit/test_health.py
from fastapi.testclient import TestClient
from ...app.main import app

client = TestClient(app)

def test_liveness():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_readiness():
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data