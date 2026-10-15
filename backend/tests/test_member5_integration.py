
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_integration_report_route_registered():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    paths = response.json()["paths"]

    assert (
        "/api/v1/integration/files/{file_id}/report"
        in paths
    )


def test_integration_report_returns_404_for_missing_file():
    response = client.get(
        "/api/v1/integration/files/999999999/report"
    )

    assert response.status_code == 404
