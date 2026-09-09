import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_db
from app.models.user import Base, User, RoleEnum
from app.core.security import hash_password, create_access_token
from app.db.init_db import seed_default_users

# Use in-memory SQLite database for isolated test execution
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create fresh database tables and seed users for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    seed_default_users(db)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Override get_db dependency with testing session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# Helper to get auth header
def get_auth_header(client: TestClient, username: str, password: str = "AdminPassword123!") -> dict:
    # Use standard test passwords based on role
    passwords = {
        "admin": "AdminPassword123!",
        "analyst_sarah": "AnalystPassword123!",
        "soc_aman": "SocPassword123!",
        "researcher_mohit": "ResearcherPassword123!",
    }
    pwd = passwords.get(username, password)
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": username, "password": pwd}
    )
    assert login_res.status_code == 200, f"Login failed for {username}: {login_res.text}"
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------
# Test Cases
# ---------------------------------------------------------

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_user_registration(client):
    payload = {
        "email": "new_analyst@threatlens.ai",
        "username": "new_analyst",
        "full_name": "New Analyst",
        "password": "SecurePassword123!",
        "role": RoleEnum.SECURITY_ANALYST.value,
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new_analyst@threatlens.ai"
    assert data["role"] == "Security Analyst"
    assert "file:upload" in data["permissions"]


def test_user_registration_duplicate(client):
    payload = {
        "email": "admin@threatlens.ai", # Already seeded
        "username": "admin_duplicate",
        "password": "Password123!",
        "role": RoleEnum.ADMINISTRATOR.value,
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_success(client):
    payload = {
        "username_or_email": "admin",
        "password": "AdminPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "admin"
    assert data["user"]["role"] == "Administrator"


def test_login_invalid_password(client):
    payload = {
        "username_or_email": "admin",
        "password": "WrongPassword!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_get_current_user_profile(client):
    headers = get_auth_header(client, "analyst_sarah")
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "analyst_sarah"
    assert data["role"] == "Security Analyst"
    assert "scan:static" in data["permissions"]


def test_refresh_token_endpoint(client):
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "soc_aman", "password": "SocPassword123!"}
    )
    refresh_token = login_res.json()["refresh_token"]

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


# ---------------------------------------------------------
# Role-Based Access Control (RBAC) Tests
# ---------------------------------------------------------

def test_admin_access_allowed(client):
    headers = get_auth_header(client, "admin")
    # Admin can access admin console
    response = client.get("/api/v1/admin/dashboard", headers=headers)
    assert response.status_code == 200
    assert response.json()["role"] == "Administrator"


def test_analyst_cannot_access_admin_dashboard(client):
    headers = get_auth_header(client, "analyst_sarah")
    # Analyst attempting to access admin dashboard -> 403 Forbidden
    response = client.get("/api/v1/admin/dashboard", headers=headers)
    assert response.status_code == 403
    assert "Access forbidden" in response.json()["detail"]


def test_analyst_access_scans(client):
    headers = get_auth_header(client, "analyst_sarah")
    # Analyst can access analyst scans
    response = client.get("/api/v1/analyst/scans", headers=headers)
    assert response.status_code == 200
    assert response.json()["role"] == "Security Analyst"


def test_soc_access_threat_feed(client):
    headers = get_auth_header(client, "soc_aman")
    # SOC can access SOC threat feed
    response = client.get("/api/v1/soc/threat-feed", headers=headers)
    assert response.status_code == 200
    assert response.json()["role"] == "SOC Team Member"

    # SOC member cannot access analyst scans -> 403 Forbidden
    forbidden_res = client.get("/api/v1/analyst/scans", headers=headers)
    assert forbidden_res.status_code == 403


def test_researcher_access_workspace(client):
    headers = get_auth_header(client, "researcher_mohit")
    # Researcher can access research samples
    response = client.get("/api/v1/researcher/samples", headers=headers)
    assert response.status_code == 200
    assert response.json()["role"] == "Researcher"

    # Researcher cannot access admin dashboard -> 403 Forbidden
    forbidden_res = client.get("/api/v1/admin/dashboard", headers=headers)
    assert forbidden_res.status_code == 403


def test_granular_permission_check(client):
    # SOC member has 'logs:monitor' permission
    headers = get_auth_header(client, "soc_aman")
    response = client.get("/api/v1/audit/logs", headers=headers)
    assert response.status_code == 200

    # Researcher does NOT have 'logs:monitor' permission -> 403 Forbidden
    res_headers = get_auth_header(client, "researcher_mohit")
    forbidden_res = client.get("/api/v1/audit/logs", headers=res_headers)
    assert forbidden_res.status_code == 403
    assert "Missing required permission" in forbidden_res.json()["detail"]
