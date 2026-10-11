# ThreatLens-AI — Dual-Engine Threat Intelligence Platform

![React](https://img.shields.io/badge/React-18.x-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random%20Forest-F7931E?logo=scikitlearn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**ThreatLens-AI** is an enterprise-grade, Dual-Engine Threat Intelligence and Malware Analysis Platform engineered for Security Operations Centers (SOC) and Incident Response teams. The platform bridges the gap between deterministic heuristic scanning and probabilistic artificial intelligence, delivering sub-millisecond threat predictions and actionable containment playbooks for suspicious binaries.

---

## 📚 Complete Project Documentation Set

As part of **Milestone 4 (Project Documentation & Platform Engineering)**, a complete, enterprise-grade documentation suite has been curated for operators, developers, and evaluators:

| Documentation Guide | Description |
|---|---|
| 📑 [**Master Documentation Index**](docs/README.md) | Central documentation directory, sitemap, and platform executive summary. |
| 🏛️ [**Architecture Notes & System Design**](docs/ARCHITECTURE_NOTES.md) | High-level architecture, component hierarchy, technical trade-offs, and data lifecycle diagrams. |
| 🔬 [**Complete Technical Documentation**](docs/TECHNICAL_DOCUMENTATION.md) | Full technical specifications: static PE analysis, YARA rules, 55+ ClaMP ML features, Random Forest pipeline, and complete REST API references. |
| 🛡️ [**SOC Analyst User Guide & Manual**](docs/USER_GUIDE.md) | End-to-end operator manual: role-based logins, dashboard navigation, upload workflow, threat report analysis, and incident response playbooks. |
| 🐳 [**Docker & Deployment Guide**](docs/DEPLOYMENT_GUIDE.md) | Multi-container Docker orchestration (`docker-compose`), environment variables, healthchecks, Nginx reverse proxy, and cloud production hardening. |
| 🧪 [**Testing, QA & Benchmark Validation Report**](docs/TESTING_AND_QA_REPORT.md) | Test coverage matrices, automated pytest suites, bug tracking log, and sub-millisecond AI latency benchmark proofs. |

---

## 🚀 Key Architectural Capabilities

### 1. Dual-Engine Threat Detection Pipeline
* **Engine 1 (Deterministic Static & YARA Engine):** Rapidly parses Portable Executable (PE) headers, sections, and import tables. Flags suspicious Windows APIs (`VirtualAlloc`, `WriteProcessMemory`, `CreateRemoteThread`) and matches known malware signatures via custom YARA rules (WannaCry, Mimikatz, Registry Persistence).
* **Engine 2 (Machine Learning Behavioral Classifier):** Employs an optimized Scikit-Learn **Random Forest Classifier** trained on 55+ quantitative features from the ClaMP dataset. Predicts zero-day and polymorphic malware in `< 0.001s` without code execution.
* **Behavioral Fusion Service:** Merges static indicators, YARA evidence, and ML confidence into a normalized **Risk Score (0–100)** and prescribes immediate incident response actions.

### 2. Real-Time SOC Dashboard
* **Dynamic Security KPIs:** Live tracking of total files scanned, active threats detected, clean files, and AI prediction accuracy.
* **Visual Threat Analytics:** Visual distribution of malware families (Trojans, Ransomware, Credential Stealers) and risk levels (Critical, High, Medium, Low).
* **Recent Telemetry Feed:** Real-time stream of analyzed binaries with one-click SHA-256 hash copying and deep links to full forensic reports.

### 3. Professional SOC Ergonomics
* Synchronized Light and Dark themes with WCAG AA compliance.
* Type-safe nested evidence rendering for complex YARA matches.
* Instant toast notification alerts on high-severity threat detections.

---

## ⚡ Quickstart & Deployment

### Option A: Running with Docker Compose (Recommended)
Launch the entire platform (FastAPI backend + React frontend) in isolated microservice containers:

```bash
# 1. Clone the repository and configure environment
git clone https://github.com/rajdeep-r24/ThreatLens-AI.git
cd ThreatLens-AI
cp .env.example .env

# 2. Build and launch services
docker compose up --build
```
* **Frontend Application:** `http://localhost:5173`
* **FastAPI Interactive Docs:** `http://localhost:8000/docs`

---

### Option B: Running Locally (Development Mode)

#### 1. Start the FastAPI Backend
```bash
cd backend

# Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies and start server
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Start the React Frontend
```bash
cd frontend

# Install packages and start dev server
npm install
npm run dev
```

---

## 🔑 Demonstration Accounts

The platform includes four pre-seeded accounts configured for role-based evaluation:

| Role | Username | Password | Access Scope |
|---|---|---|---|
| **Administrator** | `admin` | `AdminPassword123!` | Global administration, user management, system metrics |
| **Security Analyst** | `analyst_sarah` | `AnalystPassword123!` | File upload, deep scanning, detailed report review |
| **SOC Team** | `soc_aman` | `SocPassword123!` | Monitoring dashboard, live feeds, threat alerts |
| **Researcher** | `researcher_mohit` | `ResearcherPassword123!` | Raw PE inspection, YARA signature analysis, JSON export |

---

## 🧪 Automated Testing & Verification

Run the comprehensive automated test suite covering authentication, RBAC, static heuristics, ML pipelines, and behavioral fusion:

```bash
cd backend
pytest -v
```


## 📜 Disclaimer
ThreatLens-AI is intended for educational, research, and authorized cybersecurity threat analysis. Always analyze potentially malicious binaries in an isolated, secure environment.
