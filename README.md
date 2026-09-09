# ThreatLens AI

**ThreatLens AI** is an AI-powered malware classification and threat detection system that analyzes suspicious files, extracts structural indicators, matches signatures, and evaluates risk scores.

---

## 📌 Milestone 1 Overview

Milestone 1 establishes the core foundation of the platform:
- **Authentication & RBAC**: JWT-based login with role-based access for Administrator, Security Analyst, SOC Team Member, and Researcher.
- **Database & Persistence**: SQLAlchemy models storing users, file records, static analysis reports, and YARA signature results.
- **Static Analysis Engine**: Automated file hashing (MD5, SHA-256), PE header/import analysis, ASCII string extraction, and network indicator (IP/URL) detection.
- **Web Dashboard**: Interactive dark-mode security operations dashboard with live stats and threat report inspector.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & npm

---

### 2. Start the Backend API

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn app.main:app --reload --port 8000
```

* **Swagger API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

### 3. Start the Frontend Dashboard

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

* **Web Dashboard App**: [http://localhost:3000](http://localhost:3000)

---

## 🔑 Demo Accounts for Testing

The database comes pre-seeded with accounts for all 4 roles:

| Role | Username | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Security Analyst** | `analyst_sarah` | `AnalystPassword123!` | File uploads, static analysis scans, reports |
| **Administrator** | `admin` | `AdminPassword123!` | User management, settings, policies |
| **SOC Team Member** | `soc_aman` | `SocPassword123!` | Detection logs, active threat tracking |
| **Researcher** | `researcher_mohit` | `ResearcherPassword123!` | Sample analysis, threat intelligence |

---

## 🧪 Running Automated Tests

To verify backend endpoints and authentication guards:

```bash
cd backend
python -m pytest tests/ -v
```
