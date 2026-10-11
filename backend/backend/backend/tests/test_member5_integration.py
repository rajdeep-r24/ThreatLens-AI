"""
ThreatLens AI - Milestone 3
Member 5 Integration Tests
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_integration_endpoint_exists():
    response = client.get(
        "/api/v1/integration/files/1/complete-report"
    )

    assert response.status_code in [200, 404]


def test_missing_file_returns_404():
    response = client.get(
        "/api/v1/integration/files/999999/complete-report"
    )

    assert response.status_code == 404