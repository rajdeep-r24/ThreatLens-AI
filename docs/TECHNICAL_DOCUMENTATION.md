# ThreatLens-AI — Complete Technical Documentation

## 1. Technical Overview

ThreatLens-AI is a high-throughput, dual-engine malware analysis and threat intelligence platform designed for automated triage of suspicious executables. The backend is built on **FastAPI (Python 3.12)** utilizing **SQLAlchemy** for persistence and **Scikit-Learn** for machine learning inference. The frontend is built on **React 18** with **Vite** and **Tailwind CSS**.

---

## 2. Engine 1: Static Heuristic & YARA Analysis

The static analysis pipeline evaluates binaries in memory without code execution, extracting deterministic artifacts across four modular inspection layers:

### 2.1. Cryptographic Hashing
For every submitted binary, the platform computes:
* **MD5:** Fast hash verification for legacy IOC lookups.
* **SHA-256:** Cryptographically secure identifier used as the primary threat indexing key across all platform records.

### 2.2. PE Header & Structural Extraction
Utilizing `pefile`, the engine parses the Portable Executable structure:
* **COFF & Optional Headers:** Machine type, timestamp, subsystem, `AddressOfEntryPoint`, `ImageBase`.
* **Section Analysis:** Number of sections (`.text`, `.data`, `.rsrc`, `.reloc`), section entropy, and virtual vs. raw size ratios (to detect packing/compression).
* **Import Table Parsing (IAT):** Discovers dynamically linked libraries (`KERNEL32.DLL`, `ADVAPI32.DLL`, `WS2_32.DLL`) and imported API function symbols.

### 2.3. Suspicious API Signature Detection
Malicious binaries frequently employ specific Windows API calls to evade defenses or achieve privilege escalation. The engine cross-references imports against a curated threat catalog:

| Target API Function | Malicious Technique Classification |
|---|---|
| `VirtualAlloc`, `VirtualProtect` | Memory allocation for shellcode injection / unpacking |
| `WriteProcessMemory`, `CreateRemoteThread` | Process injection / DLL hollowing |
| `OpenProcess`, `AdjustTokenPrivileges` | Token theft / privilege escalation (`SeDebugPrivilege`) |
| `RegSetValueEx` | Persistence via Run / RunOnce registry keys |
| `URLDownloadToFile`, `WinExec`, `ShellExecute` | Secondary payload staging / dropper behavior |
| `SetWindowsHookEx` | Keylogging / user event hooking |

### 2.4. Suspicious String & Indicator Extraction
The engine extracts ASCII and Unicode printable byte sequences (minimum length: 4 characters) and filters for high-fidelity indicators:
* **Execution artifacts:** `powershell`, `cmd.exe`, `wscript`, `invoke-expression`, `downloadstring`.
* **Credential dumping strings:** `mimikatz`, `sekurlsa`, `lsass.exe`, `wdigest`.
* **Evasion keywords:** `bypass`, `hidden`, `reg add`.
* **Network Indicators:** Regular expression matching identifies extracted IPv4 addresses and fully qualified domain names (URLs).

### 2.5. Custom YARA Signature Engine
The platform includes custom YARA rules targeting specific malware families:
```yara
rule WannaCry_Ransomware_Indicators {
    meta:
        description = "Detects characteristic WannaCry ransomware strings"
        severity = "critical"
        threat_family = "Ransomware"
    strings:
        $s1 = "WanaCrypt0r" ascii wide
        $s2 = "tasksche.exe" ascii
        $s3 = "mssecsvc.exe" ascii
    condition:
        2 of ($s*)
}

rule Mimikatz_Credential_Dump {
    meta:
        description = "Detects in-memory credential harvesting tool artifacts"
        severity = "critical"
        threat_family = "CredentialStealer"
    strings:
        $str1 = "sekurlsa::logonpasswords" ascii wide
        $str2 = "lsass.exe" ascii wide nocase
        $str3 = "privilege::debug" ascii wide
    condition:
        any of ($str*)
}

rule Persistence_Registry_Modification {
    meta:
        description = "Detects Windows auto-start run key registry strings"
        severity = "medium"
        threat_family = "Persistence"
    strings:
        $reg = "Software\\Microsoft\\Windows\\CurrentVersion\\Run" ascii nocase
    condition:
        $reg
}
```

---

## 3. Engine 2: Machine Learning Prediction Pipeline

### 3.1. Training Dataset & Feature Engineering
Engine 2 is trained on the **ClaMP (Classification of Malware with PE features)** dataset. Instead of fragile byte signatures, it evaluates 55 quantitative structural features:

* **DOS Header Features (6):** `e_cblp`, `e_cp`, `e_cparhdr`, `e_maxalloc`, `e_sp`, `e_lfanew`.
* **File Header Features (13):** `NumberOfSections`, `CreationYear`, `FH_char0` through `FH_char14`.
* **Optional Header Features (28):** `MajorLinkerVersion`, `MinorLinkerVersion`, `SizeOfCode`, `SizeOfInitializedData`, `SizeOfUninitializedData`, `AddressOfEntryPoint`, `BaseOfCode`, `BaseOfData`, `ImageBase`, `MajorOperatingSystemVersion`, `MinorOperatingSystemVersion`, `MajorImageVersion`, `MinorImageVersion`, `MajorSubsystemVersion`, `MinorSubsystemVersion`, `SizeOfImage`, `SizeOfHeaders`, `CheckSum`, `Subsystem`, `OH_DLLchar0` through `OH_DLLchar9`, `SizeOfStackReserve`, `SizeOfStackCommit`, `SizeOfHeapReserve`, `SizeOfHeapCommit`, `LoaderFlags`.
* **Section & Entropy Statistics (8):** `sus_sections`, `non_sus_sections`, `packer`, `packer_type`, `E_text`, `E_data`, `E_file`, `filesize`.

### 3.2. Model Pipeline Architecture
The machine learning model is encapsulated within a Scikit-Learn `Pipeline` saved as `models/malware_classifier_pipeline.joblib`:

```
Raw PE Binary
      │
      ▼
pefile Feature Extraction (55 features)
      │
      ▼
ColumnTransformer
   ├── Numerical Features ──> StandardScaler
   └── Categorical Features ─> OneHotEncoder
      │
      ▼
RandomForestClassifier (Ensemble Decision Trees)
      │
      ├── predict()       ──> 1 (Malware) or 0 (Benign)
      └── predict_proba() ──> [P(Benign), P(Malware)] -> Confidence Score
```

* **Algorithm:** Random Forest Classifier (ensemble of decision trees).
* **Latency:** Benchmarked at `< 0.001 seconds` per sample inference.
* **Accuracy:** > 96% validation accuracy on the ClaMP benchmark test split.

---

## 4. Behavioral Fusion & Unified Threat Scoring

To ensure deterministic reliability, the outputs of Engine 1 and Engine 2 are unified by the Behavioral Fusion Service:

```python
# Unified Scoring Formula
risk_score = 0

if is_pe:
    risk_score += 20  # Executable baseline weight

if matched_suspicious_apis:
    risk_score += min(len(matched_suspicious_apis) * 15, 45)

if matched_suspicious_strings:
    risk_score += min(len(matched_suspicious_strings) * 10, 30)

if network_indicators.get("urls") or network_indicators.get("ips"):
    risk_score += 15

risk_score = min(risk_score, 100)

# Fusion with Machine Learning Engine
if ml_prediction == "Malware":
    ml_confidence_pct = int(ml_confidence * 100)
    final_risk_score = max(risk_score, ml_confidence_pct)
else:
    final_risk_score = risk_score
```

### Risk Stratification & Prescribed Actions

| Risk Score | Threat Level | Default Classification | Prescribed SOC Action |
|---|---|---|---|
| **80 – 100** | **Critical** | High Risk Trojan / Malware | Quarantine host immediately, terminate associated process trees, escalate to IR. |
| **50 – 79** | **High / Medium** | Suspicious Binary / Threat | Isolate binary, trigger dynamic sandbox execution, monitor network perimeter. |
| **30 – 49** | **Medium / Low** | Low Risk Unclassified File | Monitor host telemetry, flag in SIEM log aggregator. |
| **0 – 29** | **Low** | Benign Clean Document | Mark safe for endpoint execution. No further action. |

---

## 5. Database Schema & Models

ThreatLens-AI utilizes SQLAlchemy with a relational SQLite database schema (`threatlens.db`):

```
+---------------------------------------------------------------------------------+
|                                    users                                        |
+-------------------+------------------+------------------------------------------+
| id                | INTEGER          | PRIMARY KEY, AUTOINCREMENT               |
| email             | VARCHAR(255)     | UNIQUE, NOT NULL, INDEXED                |
| username          | VARCHAR(100)     | UNIQUE, NOT NULL, INDEXED                |
| full_name         | VARCHAR(255)     | NULLABLE                                 |
| hashed_password   | VARCHAR(255)     | NOT NULL (bcrypt hashed)                 |
| role              | VARCHAR(50)      | NOT NULL (admin, analyst, soc, etc.)     |
| is_active         | BOOLEAN          | DEFAULT TRUE                             |
| created_at        | DATETIME         | DEFAULT CURRENT_TIMESTAMP                |
+-------------------+------------------+------------------------------------------+
         |
         | 1-to-many
         v
+---------------------------------------------------------------------------------+
|                                    files                                        |
+-------------------+------------------+------------------------------------------+
| id                | INTEGER          | PRIMARY KEY, AUTOINCREMENT               |
| user_id           | INTEGER          | FOREIGN KEY (users.id), NULLABLE         |
| filename          | VARCHAR(255)     | NOT NULL                                 |
| file_path         | VARCHAR(500)     | NOT NULL                                 |
| file_size         | INTEGER          | NOT NULL (in bytes)                      |
| md5_hash          | VARCHAR(32)      | INDEXED, NOT NULL                        |
| sha256_hash       | VARCHAR(64)      | INDEXED, NOT NULL                        |
| file_type         | VARCHAR(100)     | NULLABLE                                 |
| status            | VARCHAR(50)      | DEFAULT "pending" (pending/completed)   |
| created_at        | DATETIME         | DEFAULT CURRENT_TIMESTAMP                |
+-------------------+------------------+------------------------------------------+
         |
         | 1-to-1                          1-to-many
         +-----------------------+-----------------------------+
         v                                                     v
+-----------------------------------------+   +------------------------------------+
|            analysis_results             |   |            yara_results            |
+---------------------+-------------------+   +--------------------+---------------+
| id                  | INTEGER (PK)      |   | id                 | INTEGER (PK)  |
| file_id             | INTEGER (FK, UNQ) |   | file_id            | INTEGER (FK)  |
| pe_headers          | JSON              |   | rule_name          | VARCHAR(100)  |
| extracted_strings   | JSON (List)       |   | severity           | VARCHAR(50)   |
| suspicious_apis     | JSON (List)       |   | tags               | JSON (List)   |
| network_indicators  | JSON              |   | matched_strings    | JSON (List)   |
| risk_score          | INTEGER           |   | created_at         | DATETIME      |
| threat_class        | VARCHAR(100)      |   +--------------------+---------------+
| recommended_action  | VARCHAR(255)      |
| ml_prediction       | VARCHAR(50)       |
| ml_confidence       | FLOAT             |
| scan_duration       | FLOAT             |
| created_at          | DATETIME          |
+---------------------+-------------------+
```

---

## 6. Complete REST API Reference

All API routes are served under prefix `/api/v1`.

### 6.1. Authentication Endpoints

#### `POST /api/v1/auth/login`
Authenticates a user and issues JWT bearer tokens.
* **Request Body:** Form data or JSON (`username`, `password`)
* **Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "user": {
    "id": 2,
    "username": "analyst_sarah",
    "email": "analyst@threatlens.ai",
    "role": "security_analyst"
  }
}
```

#### `GET /api/v1/auth/me`
Retrieves the profile and role privileges of the currently authenticated user.
* **Headers:** `Authorization: Bearer <access_token>`

---

### 6.2. File Upload & Scan Endpoints

#### `POST /api/v1/files/upload`
Uploads a binary sample and triggers immediate dual-engine analysis.
* **Request:** `multipart/form-data` with `file: <binary>`
* **Response (200 OK):**
```json
{
  "id": 12,
  "filename": "suspicious_payload.exe",
  "file_size": 245800,
  "md5_hash": "5d41402abc4b2a76b9719d911017c592",
  "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "status": "completed",
  "analysis": {
    "risk_score": 85,
    "threat_classification": "High Risk Trojan / Malware",
    "recommended_action": "Quarantine Immediately & Escalate to Security Analyst",
    "ml_prediction": "Malware",
    "ml_confidence": 0.942,
    "scan_duration": 0.04
  }
}
```

#### `GET /api/v1/files`
Returns a paginated list of all scanned files and high-level verdicts.
* **Query Parameters:** `skip=0`, `limit=20`

#### `GET /api/v1/files/{file_id}`
Returns full detailed inspection metadata, PE headers, imports, and YARA matches for a file ID.

---

### 6.3. AI Intelligence & Prediction Reports

#### `GET /api/v1/predictions/{file_id}/report`
Executes behavioral fusion analysis and generates a complete SOC intelligence report.
* **Response (200 OK):**
```json
{
  "threat_report": {
    "report_metadata": {
      "filename": "suspicious_payload.exe",
      "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "generated_at": "2026-10-12T01:40:00Z"
    },
    "threat_assessment": {
      "final_threat_score": 85,
      "threat_level": "Critical",
      "threat_category": "Trojan / Backdoor",
      "ml_prediction": "Malware",
      "ml_confidence": 0.942,
      "behavioral_findings": [
        "Dynamic Process Injection APIs detected",
        "Registry Persistence string matched"
      ],
      "recommended_action": "Quarantine host immediately and review outbound connections"
    }
  },
  "notification": {
    "type": "Security Warning",
    "severity": "Critical",
    "message": "Critical severity threat detected in suspicious_payload.exe."
  },
  "status_update": {
    "filename": "suspicious_payload.exe",
    "status": "Completed"
  }
}
```

---

### 6.4. Dashboard & Telemetry Endpoints

#### `GET /api/v1/dashboard/stats`
Returns aggregated KPI counts across the entire platform.
* **Response (200 OK):**
```json
{
  "total_scans": 142,
  "threats_detected": 38,
  "clean_files": 104,
  "average_threat_score": 34.2,
  "accuracy_rate": 96.8
}
```
