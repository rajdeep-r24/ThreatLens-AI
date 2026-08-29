import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_api_endpoints():
    print("Testing Backend API Endpoints (Member 1 Database & Architecture)...")
    
    # Health check
    res = client.get("/api/health")
    assert res.status_code == 200
    print("[PASS] GET /api/health ->", res.json())

    # Get users
    res = client.get("/api/users")
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 4
    print(f"[PASS] GET /api/users -> Found {len(users)} users with roles: {[u['role'] for u in users]}")

    # Dashboard stats
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    stats = res.json()
    print("[PASS] GET /api/dashboard/stats ->", stats)

    # Get files list
    res = client.get("/api/files")
    assert res.status_code == 200
    files = res.json()
    assert len(files) >= 3
    print(f"[PASS] GET /api/files -> Listed {len(files)} files: {[f['filename'] for f in files]}")

    # Get file detail
    res = client.get("/api/files/1")
    assert res.status_code == 200
    file_detail = res.json()
    assert file_detail["filename"] == "invoice.exe"
    assert file_detail["analysis_result"]["risk_score"] == 82
    assert len(file_detail["yara_results"]) >= 2
    print("[PASS] GET /api/files/1 -> Successfully fetched detail for invoice.exe")
    print("\nALL BACKEND API TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_api_endpoints()
