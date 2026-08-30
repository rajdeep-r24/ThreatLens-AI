import sys
import os

# Add paths for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

try:
    from app.main import app
except ImportError:
    from backend.app.main import app

from fastapi.testclient import TestClient

client = TestClient(app)


def test_api_endpoints():
    print("Testing Backend API Endpoints (Member 1 & Member 3 Integration)...")
    
    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200
    print("[PASS] GET /api/health ->", res.json())

    # 2. Health root check
    res = client.get("/health")
    assert res.status_code == 200
    print("[PASS] GET /health ->", res.json())

    # 3. Roles Permission Matrix
    res = client.get("/api/v1/auth/roles-matrix")
    assert res.status_code == 200
    roles = res.json()
    assert "Administrator" in roles
    assert "Security Analyst" in roles
    print(f"[PASS] GET /api/v1/auth/roles-matrix -> Verified all {len(roles)} roles")

    # 4. Dashboard stats
    res = client.get("/api/v1/dashboard/stats")
    assert res.status_code == 200
    stats = res.json()
    assert stats["total_scans"] >= 3
    print("[PASS] GET /api/v1/dashboard/stats ->", stats)

    # 5. Get files list
    res = client.get("/api/v1/files")
    assert res.status_code == 200
    files = res.json()
    assert len(files) >= 3
    print(f"[PASS] GET /api/v1/files -> Listed {len(files)} files: {[f['filename'] for f in files]}")

    # 6. Get file detail
    res = client.get("/api/v1/files/1")
    assert res.status_code == 200
    file_detail = res.json()
    assert file_detail["filename"] == "invoice.exe"
    assert file_detail["analysis_result"]["risk_score"] == 82
    assert len(file_detail["yara_results"]) >= 2
    print("[PASS] GET /api/v1/files/1 -> Successfully fetched detail for invoice.exe")
    
    print("\nALL BACKEND API INTEGRATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_api_endpoints()
