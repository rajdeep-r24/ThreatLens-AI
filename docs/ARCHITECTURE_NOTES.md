# ThreatLens-AI — Architecture Notes & System Design

## 1. Executive Summary

**ThreatLens-AI** is architected as an enterprise-grade, dual-engine threat intelligence and malware classification platform. Traditional antivirus engines suffer from an asymmetric disadvantage: signature-based mechanisms fail against zero-day threats and polymorphic malware, while pure black-box deep learning models lack interpretability and require excessive compute overhead.

ThreatLens-AI reconciles this trade-off through a **hybrid dual-engine architecture**:
1. **Deterministic Static & Heuristic Engine:** Leverages structural PE parsing, cryptographic hashing, suspicious Windows API extraction, and custom YARA pattern matching to rapidly catch known threats.
2. **Probabilistic Machine Learning Engine:** Employs a Scikit-Learn **Random Forest Classifier** trained on the ClaMP (Classification of Malware with PE features) dataset to analyze 55+ structural binary attributes, identifying zero-day behavioral anomalies with sub-millisecond inference time.

The system is deployed as a decoupled microservices architecture with a reactive React/Vite frontend and an asynchronous Python FastAPI backend.

---

## 2. High-Level System Architecture

```
+-----------------------------------------------------------------------------------+
|                                 PRESENTATION TIER                                 |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                           React 18 Single Page App                          |  |
|  |                                                                             |  |
|  |  +---------------------+   +---------------------+   +--------------------+ |  |
|  |  | Security Dashboard  |   |  Upload & Deep Scan |   |  Threat Reports &  | |  |
|  |  | (KPIs, Charts, Feed)|   |  (Drag/Drop, Real-  |   |  AI Intelligence   | |  |
|  |  |                     |   |   time progress)    |   |  (YARA & ML View)  | |  |
|  |  +---------------------+   +---------------------+   +--------------------+ |  |
|  |                                                                             |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  |       State & Design: Tailwind CSS, Lucide Icons, Recharts, API Client |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST (Vite Proxy: Port 5173 -> 8000)
                                           v
+-----------------------------------------------------------------------------------+
|                                 APPLICATION TIER                                  |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                         FastAPI Core Application Server                      |  |
|  |                                                                             |  |
|  |  +-----------------+  +------------------+  +----------------------------+  |  |
|  |  | Auth & RBAC     |  | Files & Upload   |  | Predictions & Intelligence |  |  |
|  |  | (JWT, Passlib)  |  | (Hash, Metadata) |  | (Fusion & Threat Reports)  |  |  |
|  |  +-----------------+  +------------------+  +----------------------------+  |  |
|  +---------------------------------------+-------------------------------------+  |
|                                          |                                        |
|         +--------------------------------+-------------------------------+        |
|         |                                                                |        |
|         v                                                                v        |
|  +------------------------------+             +--------------------------------+  |
|  | ENGINE 1: STATIC & YARA      |             | ENGINE 2: MACHINE LEARNING     |  |
|  |                              |             |                                |  |
|  | * MD5 / SHA256 Calculations  |             | * 55+ ClaMP Feature Extractor  |  |
|  | * PE Header & Section Parser |             | * Scikit-Learn Pipeline        |  |
|  | * Suspicious API Call Filter |             | * Random Forest Classifier     |  |
|  | * String & Network Extractor |             | * Calibrated Confidence Score  |  |
|  | * Custom YARA Rules Engine   |             | * Sub-millisecond Execution    |  |
|  +--------------+---------------+             +---------------+----------------+  |
|                 |                                             |                   |
|                 +----------------------+----------------------+                   |
|                                        |                                          |
|                                        v                                          |
|  +-----------------------------------------------------------------------------+  |
|  |                       BEHAVIORAL FUSION & SCORING                           |  |
|  |                                                                             |  |
|  | * Dynamic Risk Matrix (0-100)           * Notification & Alerting Service   |  |
|  | * Threat Categorization                 * Mitigation Action Recommendation  |  |
|  +-------------------------------------+---------------------------------------+  |
+----------------------------------------|------------------------------------------+
                                         v
+-----------------------------------------------------------------------------------+
|                                   DATA TIER                                       |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                       SQLite & SQLAlchemy ORM                               |  |
|  |                                                                             |  |
|  |  [users]                 [files]                 [analysis_results]         |  |
|  |  - id, email, role       - id, filename, hashes  - risk_score, pe_headers   |  |
|  |                          - file_size, status     - ml_prediction, apis      |  |
|  |                                                                             |  |
|  |                          [yara_results]          [notifications]            |  |
|  |                          - rule_name, severity   - alert_type, message      |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Sample Ingestion & Analysis Lifecycle

The lifecycle of an uploaded binary demonstrates strict separation of concerns, non-destructive execution, and fail-safe state propagation:

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as SOC Analyst (Browser)
    participant UI as React Frontend
    participant API as FastAPI Gateway
    participant DB as SQLite Database
    participant Static as Static & YARA Engine
    participant ML as Random Forest ML Engine
    participant Fusion as Behavioral Fusion Service

    Analyst->>UI: Selects & uploads binary (e.g. invoice.exe)
    UI->>API: POST /api/v1/files/upload (multipart/form-data)
    Note over API: Validates file stream & generates storage path
    API->>DB: INSERT files (filename, hashes, size, status="scanning")
    API->>Static: run_static_analysis_pipeline(filepath)
    activate Static
    Static->>Static: Compute MD5 & SHA-256
    Static->>Static: Parse PE Headers, Sections & Imports
    Static->>Static: Match Suspicious APIs & Regex Strings
    Static->>Static: Execute YARA Signature Rules
    Static-->>API: Return static telemetry & matches
    deactivate Static

    API->>ML: extract_ml_features(filepath) -> predict_malware()
    activate ML
    ML->>ML: Extract 55 ClaMP header & section metrics
    ML->>ML: Execute Random Forest classification pipeline
    ML-->>API: Return { label: "Malware", confidence: 0.94 }
    deactivate ML

    API->>Fusion: fuse_intelligence(static_data, ml_data)
    activate Fusion
    Fusion->>Fusion: Calculate normalized Risk Score (0-100)
    Fusion->>Fusion: Assign Threat Classification & Action
    Fusion->>Fusion: Generate Security Alert Notification
    Fusion-->>API: Return unified Intelligence Report
    deactivate Fusion

    API->>DB: INSERT analysis_results & yara_results; UPDATE status="completed"
    API-->>UI: Return HTTP 200 with full scan payload
    UI->>Analyst: Renders Security Report & Toast Alert
```

---

## 4. Key Architectural Trade-Offs & Rationale

Every technical choice in ThreatLens-AI was driven by concrete operational requirements:

### 4.1. Framework Choice: FastAPI vs Flask/Django
* **Decision:** FastAPI with Uvicorn ASGI server.
* **Rationale:** FastAPI provides native asynchronous request processing (`async def`), automated OpenAPI 3.0 (Swagger) generation, and Pydantic schema validation. In security platforms handling streaming binary uploads and concurrent analysis, FastAPI delivers significantly higher I/O throughput and lower memory footprint compared to synchronous Flask or bloated Django setups.

### 4.2. Frontend Framework: React 18 + Vite vs SSR / Server Templates
* **Decision:** React 18 SPA bundled with Vite and styled via Tailwind CSS.
* **Rationale:** SOC analysts interact with live telemetry feeds, real-time KPI re-renders, and interactive collapsible JSON evidence trees. A reactive component model allows granular sub-tree re-rendering without full page refreshes. Vite ensures sub-300ms development server startup and optimized tree-shaken production bundles.

### 4.3. Machine Learning Paradigm: Random Forest vs Deep Neural Networks
* **Decision:** Scikit-Learn Random Forest Classifier trained on ClaMP PE features.
* **Rationale:**
  1. **Inference Latency:** Deep Learning models (e.g., LSTMs or 1D-CNNs for raw bytes) require substantial GPU acceleration and exhibit high inference latency (50–500ms). Our Random Forest pipeline operates in `< 0.001s` on standard CPU cores.
  2. **Interpretability:** Security teams reject black-box verdicts. Random Forest feature importances can be audited, showing which PE attributes (e.g., section entropy, uninitialized data size) drove the classification.
  3. **Robustness to Overfitting:** Ensemble bagging over multiple decision trees mitigates overfitting on sparse binary datasets.

### 4.4. Storage Tier: SQLite with SQLAlchemy vs PostgreSQL
* **Decision:** SQLite with SQLAlchemy ORM.
* **Rationale:** Eliminates the deployment overhead of running an external database cluster during evaluations, development, and air-gapped forensic engagements. SQLAlchemy abstracts database access, allowing instant migration to PostgreSQL or MySQL for production horizontal scaling simply by updating the `DATABASE_URL` environment variable.

---

## 5. Security & Isolation Architecture

### 5.1. Non-Destructive Static Analysis
All analysis performed by ThreatLens-AI operates strictly **without executing the target binary**. The platform reads files as passive byte streams:
- `pefile` parses file headers in user-space memory without invoking the Windows loader.
- Custom regex algorithms scan printable string buffers without executing shell interpreters.
- Files are quarantined in an isolated `uploads/` directory with strict non-executable file permissions.

### 5.2. Role-Based Access Control (RBAC)
The platform enforces granular role authorization across all endpoints:

| Role | Permissions | Use Case |
|---|---|---|
| **Administrator** | Full system control, user provisioning, global scan deletion, system telemetry. | Lead Security Engineer |
| **Security Analyst** | Upload files, initiate deep scans, review intelligence reports, acknowledge alerts. | SOC Tier 2 Analyst |
| **SOC Team** | Read-only dashboard access, monitoring threat feeds, viewing KPI telemetry. | SOC Tier 1 Monitoring |
| **Researcher** | Access raw PE header dumps, download YARA matches, export behavioral JSON. | Malware Researcher / Reverse Engineer |

---

## 6. Resilience & Fault Tolerance Strategies

1. **Graceful Binary Degradation:** When an analyst uploads a non-PE file (such as a PDF or script), the PE analyzer gracefully flags `is_pe: false`. Instead of throwing a crash, the pipeline falls back to string extraction, cryptographic hashing, and heuristic regex matching.
2. **Type-Safe Frontend Parsing:** Frontend report parsers use defensive string coercions (`String(item.matched_strings)`) to guarantee that complex nested JSON structures from YARA rules or third-party plugins cannot trigger React rendering exceptions.
3. **Containerized Network Isolation:** In the Docker Compose topology, frontend and backend communicate over a dedicated bridge network, preventing direct exposure of the backend API to untrusted network segments unless proxied.

---

## 7. Future Scalability Roadmap

* **Asynchronous Task Queue:** Transition file processing to Celery workers backed by Redis, enabling concurrent batch scanning of enterprise-scale file volumes.
* **Sandboxed Dynamic Emulation:** Integrate with automated micro-VMs (e.g., Firecracker or Cuckoo Sandbox) to capture API call traces during runtime execution.
* **STIX/TAXII Threat Intelligence Feed:** Ingest and publish automated threat telemetry to global cyber threat sharing platforms.
