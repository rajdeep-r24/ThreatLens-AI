import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_db
from app.models.user import Base
from app.db.init_db import seed_default_users, seed_sample_scans
from app.services.static_analysis import run_static_analysis_pipeline

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    seed_default_users(db)
    seed_sample_scans(db)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_static_analysis_pipeline_on_temp_file():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
        f.write("powershell.exe -ExecutionPolicy Bypass http://malicious-c2.org/beacon 192.168.1.100")
        temp_path = f.name

    try:
        results = run_static_analysis_pipeline(temp_path)
        assert results["md5_hash"] is not None
        assert results["sha256_hash"] is not None
        assert "http://malicious-c2.org/beacon" in results["network_indicators"]["urls"]
        assert "192.168.1.100" in results["network_indicators"]["ip_addresses"]
        assert results["risk_score"] > 0
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_file_upload_and_scan_endpoint(client):
    file_content = b"Simulated suspicious script powershell.exe -W Hidden http://bad-domain.xyz"
    files = {"file": ("test_sample.ps1", file_content, "text/plain")}

    res = client.post("/api/v1/files/upload", files=files)
    assert res.status_code == 201
    data = res.json()
    assert data["filename"] == "test_sample.ps1"
    assert data["sha256_hash"] is not None
    assert data["analysis_result"]["risk_score"] > 0
