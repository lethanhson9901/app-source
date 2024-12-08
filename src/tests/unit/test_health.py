import pytest
from fastapi.testclient import TestClient

from src.app.main import app  # Fixed import path


@pytest.fixture
def client() -> TestClient:  # Added return type annotation
    """Fixture for creating a test client."""
    return TestClient(app)


@pytest.mark.unit
def test_health_check(client: TestClient) -> None:
    """
    Test that the health check endpoint:
    - Returns 200 OK status
    - Returns correct JSON response with 'ok' status
    """
    response = client.get("/health")

    assert response.status_code == 200, "Health check should return 200 OK"  # nosec
    response_data = response.json()
    assert response_data == {"status": "ok"}, "Health check should return status 'ok'"  # nosec


@pytest.mark.unit
def test_health_check_ready(client: TestClient) -> None:
    """
    Test that the readiness check endpoint:
    - Returns 200 OK status
    - Contains required fields in response
    - Has correct data types for all fields
    - Reports status of all required services
    """
    response = client.get("/health/ready")

    assert response.status_code == 200, "Readiness check should return 200 OK"  # nosec

    data = response.json()
    assert "status" in data, "Response should contain 'status' field"  # nosec
    assert "checks" in data, "Response should contain 'checks' field"  # nosec
    assert isinstance(data["checks"], dict), "'checks' should be a dictionary"  # nosec

    # Verify all required services are present
    required_services = {"database", "redis", "api"}
    actual_services = set(data["checks"].keys())

    assert required_services.issubset(
        actual_services
    ), f"Missing required services. Expected {required_services}, got {actual_services}"  # nosec

    # Verify all service statuses are boolean
    for service, status in data["checks"].items():
        assert isinstance(status, bool), f"Status for {service} should be boolean"  # nosec
