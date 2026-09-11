# ThreatLens-AI — Week 1 Milestone

**Team 2** | **Milestone 1** | **Member 6 — Kandela Vamshi**

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![YARA](https://img.shields.io/badge/YARA-Signature%20Engine-red?logo=files&logoColor=white)
![yara--python](https://img.shields.io/badge/yara--python-integrated-orange)
![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white)
![Git](https://img.shields.io/badge/Git-version%20control-F05032?logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-collaboration-181717?logo=github&logoColor=white)
![Status](https://img.shields.io/badge/status-completed-brightgreen)

---

## Module: YARA & Signature Detection Engine

**Branch:** `feat/yara-signature-engine`
**Assigned to:** Kandela Vamshi (Member 6, Team 2)

### Task Description

Build the signature-based malware detection component of ThreatLens-AI using YARA. This module scans files for known malicious patterns (trojans, ransomware, webshells), extracts match details, and prepares results for integration with the rest of the static analysis pipeline.

### What Was Implemented

- **YARA rule set** (`yara_rules/custom_rules.yar`) covering three threat categories:
  - Trojan detection — suspicious command execution patterns, packed PE indicators
  - Ransomware detection — ransom note strings, crypto API usage patterns
  - Webshell detection — PHP and ASPX webshell patterns
- **Scanner module** (`yara_scanner.py`) that:
  - Compiles and runs YARA rules against a target file
  - Captures matched rule names, category tags, severity, and the specific matched strings with byte offsets
  - Provides `combine_results()` to merge YARA output with static analysis output from the rest of the pipeline
- **Database model** (`models.py`) defining the `YARAResult` table — stores file reference, rule name, category, severity, matched strings, and timestamp
- **Test suite** (`tests/test_yara_scanner.py`) — automated tests covering detection across all three threat categories plus the result-combination logic

### Test Results

```
5 passed, 1 skipped
```
(The skipped test covers EICAR standard test-file detection, intentionally excluded from this submission to avoid antivirus interference during local development — the detection rule itself is included and functional.)

### Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| YARA / yara-python | Signature-based pattern matching |
| pytest | Automated testing |
| SQLAlchemy | Database model (YARAResult table) |
| Git & GitHub | Version control, branching, pull requests |
| VS Code | Development environment |

### Folder Structure

```
yara_rules/
    custom_rules.yar       # Trojan, ransomware, webshell detection rules
yara_scanner.py             # Core scan + integration logic
models.py                   # YARAResult database model
test_files/
    clean_sample.txt        # Harmless file, used to verify no false positives
tests/
    test_yara_scanner.py    # Automated test suite
```

### Notes for Integration

- `combine_results()` is ready to merge with the static analysis output produced by the rest of the pipeline — field names should be confirmed against the final schema before final merge.
- The `YARAResult` model assumes a `files` table with an `id` primary key for the foreign key relationship — aligned with the team's shared database schema.

---

**Submitted as part of Team 2's Week 1 Milestone for ThreatLens-AI.**
