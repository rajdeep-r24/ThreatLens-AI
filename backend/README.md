# ThreatLens-AI: Authentication & RBAC Module (Member 3)

This module provides the complete Authentication, Token Management, and Role-Based Access Control (RBAC) security layer for **ThreatLens-AI**.

---

## 🛡️ Role & Permissions Matrix

| Role | Default Seed Account | Password | Key Permissions |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` (`admin@threatlens.ai`) | `AdminPassword123!` | User management, settings, policies, SIEM/API integration, full dashboard access |
| **Security Analyst** | `analyst_sarah` (`analyst@threatlens.ai`) | `AnalystPassword123!` | File upload, static analysis scans, malware report review, threat monitor |
| **SOC Team Member** | `soc_alex` (`soc@threatlens.ai`) | `SocPassword123!` | Detection logs monitoring, active threats tracking, alert history, operational reports |
| **Researcher** | `researcher_elena` (`researcher@threatlens.ai`) | `ResearcherPassword123!` | Upload research samples, dataset access, malware family analysis, report export |

---

## 🚀 Quickstart Guide

### 1. Setup Virtual Environment & Install Dependencies
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux / MacOS
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run the Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
* **API Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 3. Run Automated RBAC Tests
```bash
pytest tests/test_auth_rbac.py -v
```

---

## 📡 API Endpoints

### 🔐 Authentication
* `POST /api/v1/auth/register` — Register a new user with designated role.
* `POST /api/v1/auth/login` — Authenticate with email/username and password, returns JWT tokens.
* `POST /api/v1/auth/refresh` — Issue a new access token using a valid refresh token.
* `GET /api/v1/auth/me` — Retrieve profile & permissions of the current logged-in user.
* `GET /api/v1/auth/roles-matrix` — Get full list of roles and permissions catalog.

### 🛡️ RBAC Protected Routes (Demo)
* `GET /api/v1/admin/dashboard` — Accessible only by **Administrator**.
* `GET /api/v1/analyst/scans` — Accessible by **Security Analyst** & **Administrator**.
* `GET /api/v1/soc/threat-feed` — Accessible by **SOC Team Member** & **Administrator**.
* `GET /api/v1/researcher/samples` — Accessible by **Researcher** & **Administrator**.
* `GET /api/v1/audit/logs` — Protected via granular permission: `logs:monitor`.
