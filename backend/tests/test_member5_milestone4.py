"""Member 5 - Milestone 4 integration smoke tests."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_openapi_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()


def test_api_routes_registered():
    response = client.get("/openapi.json")
    assert response.status_code == 200

    paths = response.json().get("paths", {})
    assert len(paths) > 0


def test_api_routes_have_http_methods():
    schema = client.get("/openapi.json").json()
    paths = schema.get("paths", {})

    for path, methods in paths.items():
        assert isinstance(path, str)
        assert isinstance(methods, dict)
        assert methods, f"No methods registered for {path}"