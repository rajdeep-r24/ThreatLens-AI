# ThreatLens-AI — SOC Analyst User Guide & Operator Manual

## 1. Introduction

Welcome to the **ThreatLens-AI** SOC Analyst Operator Manual. This guide provides comprehensive, practical instructions for Security Operations Center (SOC) analysts, incident responders, and threat hunters utilizing ThreatLens-AI to triage suspicious files, interpret machine learning predictions, and execute containment playbooks.

---

## 2. Authentication & Role Permissions

ThreatLens-AI utilizes JSON Web Token (JWT) role-based authentication.

### Default Demonstration Accounts
For testing, internal audits, and demonstration environments, the system includes four pre-seeded accounts:

| Role | Username | Password | Purpose & Access Level |
|---|---|---|---|
| **Administrator** | `admin` | `AdminPassword123!` | System configuration, global management, and full auditing. |
| **Security Analyst** | `analyst_sarah` | `AnalystPassword123!` | Primary operational user: upload files, run scans, review reports. |
| **SOC Team** | `soc_aman` | `SocPassword123!` | Read-only threat monitoring and live feed observation. |
| **Researcher** | `researcher_mohit` | `ResearcherPassword123!` | Forensic deep-dives, raw PE inspection, and YARA rule audits. |

### Logging In
1. Navigate to `http://localhost:5173`.
2. Enter your credentials on the login screen.
3. Upon successful validation, your session token is stored securely in local storage, and you are directed to the **Security Dashboard**.
4. The top-right navbar displays your current username and assigned role tag.

---

## 3. Navigating the Security Dashboard

The Security Dashboard provides real-time situational awareness across all endpoint and perimeter scanning activities.

```
+----------------------------------------------------------------------------------+
| ThreatLens [AI Threat Intelligence]   [Dashboard] [Upload & Scan] [Threat Reports] |
+----------------------------------------------------------------------------------+
|                                                                                  |
|  +----------------+  +----------------+  +----------------+  +----------------+  |
|  |  TOTAL SCANS   |  | THREATS FOUND  |  |  CLEAN FILES   |  |  ACCURACY RATE |  |
|  |      142       |  |       38       |  |      104       |  |     96.8%      |  |
|  +----------------+  +----------------+  +----------------+  +----------------+  |
|                                                                                  |
|  +-------------------------------------+  +-----------------------------------+  |
|  |     MALWARE DISTRIBUTION (Pie)      |  |      RISK LEVEL SEVERITY (Bar)    |  |
|  | * Trojan (42%)   * Mimikatz (28%)   |  | * Critical (18)    * High (12)    |  |
|  | * Ransomware (15%) * Clean (15%)    |  | * Medium (8)       * Low (104)    |  |
|  +-------------------------------------+  +-----------------------------------+  |
|                                                                                  |
|  +----------------------------------------------------------------------------+  |
|  |                         RECENT SCANS TELEMETRY TABLE                       |  |
|  | Filename        SHA256          Verdict       Score    Action              |  |
|  | invoice.exe     e3b0c442...     Trojan        85       [View Full Report]  |  |
|  | payload.dll     9f86d081...     Mimikatz      95       [View Full Report]  |  |
|  | document.pdf    2c26b46b...     Clean         5        [View Full Report]  |  |
|  +----------------------------------------------------------------------------+  |
+----------------------------------------------------------------------------------+
```

### Key Dashboard Components:
1. **Security KPI Metrics:**
   * **Total Scans:** Total cumulative binaries analyzed by the platform.
   * **Threats Found:** Total binaries classified as Medium, High, or Critical risk.
   * **Clean Files:** Benign files verified safe for execution.
   * **Accuracy Rate:** Historical validation accuracy of the AI classification engine.
2. **Visual Analytics:**
   * **Malware Distribution:** Visual breakdown of detected threat families (Trojans, Credential Stealers, Ransomware, Droppers).
   * **Risk Level Stratification:** Categorization across Critical, High, Medium, and Low risk thresholds.
3. **Recent Scans Telemetry Feed:** Real-time table displaying recent submissions, their cryptographic hashes, risk scores, and quick links to full intelligence reports.
4. **Analyst Ergonomics (Theme Switcher):** Click the **Sun / Moon** icon in the top navbar to toggle between synchronized Light Mode and high-contrast Dark Mode.

---

## 4. Upload & Deep Scan Workflow

### Step 1: Selecting a Sample
1. Click the **Upload & Deep Scan** tab in the main navigation bar.
2. Either drag-and-drop a target executable into the dotted upload area or click **Browse Files**.
3. **Supported Formats:**
   * PE32 / PE64 Executables (`.exe`)
   * Dynamic Link Libraries (`.dll`)
   * System Binaries (`.sys`, `.scr`)
   * Documents and Scripts (`.pdf`, `.doc`, `.vbs`, `.ps1` for static string & hash extraction).

### Step 2: Scan Execution & Telemetry
1. Click the **Initiate Dual-Engine Scan** button.
2. The UI displays an animated scanning progress indicator showing:
   * Cryptographic Hash Generation (MD5 & SHA-256)
   * Portable Executable Header & Section Parsing
   * Custom YARA Rule Pattern Matching
   * ClaMP 55-Feature Machine Learning Inference
3. Within 1 to 2 seconds, the scan completes and displays the **Executive Verdict Card**.

---

## 5. Interpreting Threat Reports & AI Intelligence

Clicking **View Full Report** or opening the **Threat Reports & AI Analysis** tab loads the deep-dive intelligence dossier for the selected binary.

### 5.1. Header Overview & IOC Identifiers
* **Filename & Size:** Identifies physical file metadata.
* **One-Click Hash Copying:** Click the copy icon next to the SHA-256 or MD5 hash to immediately copy it to your clipboard for SIEM or EDR querying.
* **Risk Score Gauge:** Displays the normalized 0–100 score with color-coded severity:
  * 🔴 **Critical (80–100):** Immediate malicious confirmation.
  * 🟠 **High (60–79):** Highly suspicious behavioral attributes.
  * 🟡 **Medium (30–59):** Heuristic anomalies requiring analyst review.
  * 🟢 **Low / Clean (0–29):** Verified safe binary.

### 5.2. Static Heuristics & YARA Evidence
Review the exact deterministic indicators that triggered alerts:
* **Triggered YARA Rules:** Lists rule names (e.g., `Mimikatz_Credential_Dump`), assigned severity, and tags.
* **Matched Byte Sequences:** Displays the literal string or hex pattern discovered in the binary (e.g., `sekurlsa::logonpasswords`).
* **Suspicious Windows APIs:** Highlights dangerous API combinations (e.g., `Kernel32.dll -> OpenProcess` + `Advapi32.dll -> AdjustTokenPrivileges`).

### 5.3. Machine Learning Behavioral Assessment
* **ML Verdict:** Displays whether the Random Forest classifier predicted `Malware` or `Benign`.
* **Confidence Level:** Shows the calibrated prediction probability (e.g., `94.2% Confidence`).
* **Behavioral Findings:** Natural language summary of structural anomalies detected by the model (e.g., uninitialized section bloat, abnormal entry point outside `.text`).

---

## 6. Recommended Incident Response Playbooks

Based on the calculated Risk Score, follow these standardized response workflows:

### Playbook A: Critical Severity (Score 80–100)
1. **Endpoint Isolation:** Immediately disconnect the host endpoint from the corporate network via your EDR platform.
2. **Process Termination:** Terminate parent and child process trees matching the reported binary.
3. **IOC Scrape:** Copy the SHA-256 hash and add it to global firewall and EDR blocklists.
4. **Credential Revocation:** If credential-stealing indicators (e.g., Mimikatz) are present, revoke and rotate all Kerberos/NTLM tickets and administrative passwords for logged-in users on that machine.

### Playbook B: High / Medium Severity (Score 30–79)
1. **Dynamic Sandbox Analysis:** Forward the sample to a sandbox environment for runtime execution and network beaconing analysis.
2. **Persistence Check:** Inspect host Run/RunOnce registry keys and Scheduled Tasks for persistence entries matching the filename.
3. **Perimeter Monitoring:** Search proxy logs for the extracted network indicators (IP addresses or URLs).

### Playbook C: Low Severity / Clean (Score 0–29)
1. **Release File:** No malicious indicators found. Mark sample as clean.

---

## 7. Troubleshooting & FAQs

### Q1: The web application shows "Unable to connect to backend server"
* **Resolution:** Ensure the FastAPI backend is running on `http://localhost:8000`. Run `uvicorn app.main:app --reload --port 8000` in the backend directory or verify the Docker container is active via `docker compose ps`.

### Q2: What happens if I upload a non-executable file (e.g., PDF or TXT)?
* **Resolution:** The platform automatically detects that the file is not a PE executable (`is_pe: false`). It disables PE-specific heuristics and runs cryptographic hashing, printable string extraction, network indicator discovery, and YARA document scanning.

### Q3: Why does the prediction run so quickly?
* **Resolution:** Machine learning inference is powered by an optimized Scikit-Learn Random Forest pipeline saved as a pre-compiled `joblib` binary. Inference takes `< 0.001s`, preventing backend bottlenecks.
