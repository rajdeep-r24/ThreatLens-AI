# ThreatLens-AI – Threat Monitoring Dashboard

## Team 2 | Member 4

**Member:** K. Vamshi  
**Role:** Threat Monitoring Dashboard Developer  
**Milestone:** Week 2 – Milestone 2

![React](https://img.shields.io/badge/React-frontend-61DAFB?logo=react&logoColor=black)
![Recharts](https://img.shields.io/badge/Recharts-data%20visualization-8884d8)
![FastAPI](https://img.shields.io/badge/FastAPI-backend%20API-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![Axios](https://img.shields.io/badge/Axios-API%20calls-5A29E4?logo=axios&logoColor=white)
![Git](https://img.shields.io/badge/Git-version%20control-F05032?logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-collaboration-181717?logo=github&logoColor=white)
![Status](https://img.shields.io/badge/status-completed-brightgreen)

---

## 📌 Overview

As part of **Team 2's ThreatLens-AI project**, I worked on the **Threat Monitoring Dashboard** during Week 2 / Milestone 2.

The dashboard consumes the threat detection and scan information provided through the backend APIs and presents it through an interactive monitoring interface.

The main goal of my contribution is to provide security analysts with a clear view of:

- Overall scan activity
- Detected threats
- Malware distribution
- Risk levels
- Threat detection trends
- Recent suspicious files

---

## 👨‍💻 My Contribution

### Threat Monitoring Dashboard

I extended the existing dashboard and implemented the following monitoring features:

- Integrated the React dashboard with backend APIs
- Added security KPI cards
- Added malware distribution visualization
- Added risk-level distribution visualization
- Added threat detection trend chart
- Added recent threats monitoring table
- Added risk classification
- Added dashboard refresh functionality
- Added automatic dashboard data refresh
- Added loading and error handling
- Integrated **Recharts** for data visualization

---

## 📊 Dashboard Features

### 1. Security KPIs

The dashboard displays important security statistics such as:

- Total Files Scanned
- Malicious Threats
- YARA Rule Matches
- Average Threat Score

These values are retrieved from the backend dashboard statistics API.

---

### 2. Malware Distribution

A visualization showing the distribution of detected malware/threat classifications.

Example classifications include:

- Potential Trojan Malware
- Credential Stealer / Mimikatz Variant
- Benign / Clean Files

---

### 3. Risk Level Distribution

Files are categorized according to their risk score:

| Risk Score | Risk Level |
|------------|------------|
| 80 – 100 | Critical |
| 60 – 79 | High |
| 30 – 59 | Medium |
| 0 – 29 | Low |

This provides a quick overview of the current threat severity.

---

### 4. Threat Detection Trend

A chart showing threat detection activity over time based on scan records received from the backend.

This helps provide a quick view of changes in threat activity.

---

### 5. Recent Threats

The dashboard displays recently analyzed files along with information such as:

- File name
- SHA256
- Threat classification
- Risk score
- YARA matches
- Risk level
- Analysis details

---

### 6. Dashboard Refresh

The dashboard supports:

- Manual refresh
- Automatic data refresh
- Last updated timestamp
- Loading state
- Error handling

This allows the dashboard to remain synchronized with the latest backend scan data.

---

## 🔄 Data Flow

```text
┌──────────────────────────────┐
│ Member 3                     │
│ Database & Scan Logging      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ FastAPI Backend              │
│                              │
│ /api/v1/dashboard/stats      │
│ /api/v1/files                │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Member 4                     │
│ React Threat Dashboard       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Security Monitoring UI       │
│                              │
│ • KPIs                       │
│ • Malware Distribution       │
│ • Risk Distribution          │
│ • Threat Trends              │
│ • Recent Threats             │
└──────────────────────────────┘
```
