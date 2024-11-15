import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add the project root directory to PYTHONPATH
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.insert(0, project_root)

from src.app.main import app

client = TestClient(app)

@pytest.mark.unit
def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.unit
def test_health_check_ready():
    """Test the readiness check endpoint."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "checks" in data
    assert isinstance(data["checks"], dict)