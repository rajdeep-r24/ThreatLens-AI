# ThreatLens-AI — Master Documentation Index

Welcome to the official documentation set for **ThreatLens-AI**, a dual-engine threat intelligence and automated malware analysis platform built for modern Security Operations Centers (SOC).

This documentation suite was curated under **Milestone 4 (Project Documentation & Platform Engineering)**, synthesizing technical findings, deployment specifications, user workflows, and test validations across all project milestones.

---

## 📚 Documentation Sitemap

| Document | Primary Audience | Description |
|---|---|---|
| [**Architecture Notes**](./ARCHITECTURE_NOTES.md) | Software Architects, Senior Engineers, Evaluators | High-level and component architecture, technical trade-offs, dual-engine design philosophy, and data lifecycle diagrams. |
| [**Technical Documentation**](./TECHNICAL_DOCUMENTATION.md) | Backend/ML Engineers, Integrators | Exhaustive technical specifications covering static heuristic engines, custom YARA rules, 55+ ClaMP feature extraction, Random Forest ML pipeline, database schemas, and complete REST API references. |
| [**SOC Analyst User Guide**](./USER_GUIDE.md) | Security Analysts, Incident Responders | Practical step-by-step operator manual for daily triage, uploading samples, interpreting risk scores, reading behavioral telemetry, and executing remediation playbooks. |
| [**Deployment & DevOps Guide**](./DEPLOYMENT_GUIDE.md) | DevOps Engineers, System Administrators | Multi-container Docker orchestration (`docker-compose`), environment configurations, networking proxies, healthchecks, and cloud production hardening. |
| [**Testing & QA Validation Report**](./TESTING_AND_QA_REPORT.md) | QA Leads, Security Auditors | Test methodology, unit/integration test matrices, workflow validation results, sub-millisecond AI prediction benchmarks, and edge-case handling. |

---

## 🎯 Platform Quick Summary

```
                      +------------------------------------+
                      |       ThreatLens-AI Frontend       |
                      |   React 18 + Vite + Tailwind CSS   |
                      |    (SOC Dashboard & Analytics)     |
                      +-----------------+------------------+
                                        |
                         REST APIs / JSON (Port 5173 -> 8000)
                                        |
                                        v
                      +------------------------------------+
                      |        FastAPI Core Backend        |
                      |      Asynchronous Python 3.12      |
                      +----+--------------------------+----+
                           |                          |
             +-------------+------------+             |
             |                          |             v
             v                          v    +-----------------+
    +-----------------+        +-----------+ |   SQLite / DB   |
    |  Engine 1:      |        | Engine 2: | | (Scan History & |
    |  Static & YARA  |        | ML AI     | |  RBAC Auth)     |
    |  - Hashes       |        | Classifier| +-----------------+
    |  - PE Headers   |        | - Random  |
    |  - Indicators   |        |   Forest  |
    |  - Byte Rules   |        | - 55+     |
    +--------+--------+        |   ClaMP   |
             |                 +-----+-----+
             |                       |
             +-----------+-----------+
                         |
                         v
             +--------------------------+
             |    Behavioral Fusion     |
             |   Threat Intelligence    |
             |   Report & Alerts        |
             +--------------------------+
```

### Core Value Proposition
1. **Zero-Day Resilience:** Traditional signature solutions miss novel binaries. ThreatLens-AI trains a Random Forest pipeline on 55+ structural PE indicators, predicting malware behavior regardless of obfuscation.
2. **Deterministic Speed:** Static heuristic analysis and custom YARA pattern matching execute in milliseconds, filtering out known threats immediately.
3. **Actionable SOC Intelligence:** Rather than delivering binary pass/fail results, the platform computes unified Risk Scores (0–100), provides behavioral capability tags, and prescribes containment playbooks.
4. **Analyst Ergonomics:** Features synchronized light/dark themes, responsive KPI metrics, real-time toast alerts, and type-safe nested report parsing.

---

## ⚡ Quickstart Commands

### Running Locally with Python & Node.js
```bash
# 1. Start the FastAPI Backend
cd backend
python -m venv .venv
.venv\Scripts\activate       # Windows (or source .venv/bin/activate on Linux/macOS)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 2. Start the React Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

### Running with Docker Compose
```bash
# Build and start all services in isolated containers
docker compose up --build
```
Navigate to `http://localhost:5173` to access the Security Dashboard and `http://localhost:8000/docs` for Swagger UI.

---

## 👥 Project Team & Contributions

This project was developed as a modular cybersecurity platform with contributions across milestones:
- **Member 1:** Application Testing, QA & Workflow Validation
- **Member 2:** UI Responsiveness, Theming & Optimization
- **Member 3:** Containerization, Docker & Cloud Deployment
- **Member 4:** Technical Documentation, User Guide & Architecture Notes
- **Member 5:** Final Integration, Evaluation Scenarios & Presentations
