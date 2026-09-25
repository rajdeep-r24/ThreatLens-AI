# ThreatLens-AI – AI Threat Analytics Dashboard

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

## Team 2 | Member 3

**Member:** K. Vamshi  
**Role:** AI Threat Analytics & Prediction Dashboard Developer  
**Milestone:** Week 3 – Milestone 3


## 📌 Overview

As part of **Team 2's ThreatLens-AI project**, I worked on the **AI Threat Analytics and Prediction Dashboard** during Week 3 / Milestone 3.

The dashboard extends the existing threat monitoring system by integrating AI-based threat prediction and report generation capabilities.

The main goal of my contribution is to provide security analysts with a clear view of:

- Threat analytics
- AI-based threat assessment
- Final threat score
- Threat category
- Recommended security action
- Behavioral threat findings
- AI-generated security summary
- Recent analyzed files

---

## 👨‍💻 My Contribution

### AI Threat Analytics & Prediction Dashboard

I extended the existing threat monitoring dashboard and implemented the following features:

- Integrated AI threat prediction report functionality
- Connected the React dashboard with prediction APIs
- Added AI Threat Prediction Report modal
- Added threat level display
- Added final threat score display
- Added threat category display
- Added recommended action display
- Added behavioral findings section
- Added AI-generated security summary
- Added loading state for AI report generation
- Added error handling for failed AI report requests
- Integrated the AI report with the existing file analysis data
- Fixed frontend-to-backend API proxy connectivity
- Tested AI report generation through the dashboard

---

## 📊 Dashboard Features

### 1. AI Threat Prediction Report

The dashboard provides an AI-generated report for analyzed files.

The report displays:

- Threat Level
- Final Threat Score
- Threat Category
- Recommended Action
- Behavioral Findings
- Security Summary

This allows analysts to understand the security implications of an analyzed file without manually reviewing every analysis result.

---

### 2. Threat Assessment

The AI report provides an overall assessment of the analyzed file.

Example information includes:

- Threat severity
- Final threat score
- Threat classification
- Security assessment

The threat assessment helps analysts quickly understand the overall security risk associated with a file.

---

### 3. Behavioral Findings

The AI report displays detected behavioral findings identified during analysis.

Each finding can include:

- Behavior name
- Severity
- Description

For example:

- YARA rule detection
- Suspicious activity
- Potential malicious behavior

---

### 4. Recommended Security Action

The AI report provides a recommended action based on the generated threat assessment.

Examples include:

- Flag for security review
- Investigate suspicious behavior
- Review before execution
- Monitor the file

This provides analysts with an immediate next-step recommendation.

---

### 5. Security Summary

The AI report includes a summarized security assessment of the analyzed file.

The summary combines the available analysis information into a readable format for security monitoring and investigation.

---

### 6. AI Report Integration

The dashboard supports:

- AI report generation
- Loading state during report generation
- API response handling
- Error handling
- Report modal display
- Closing and reopening reports

The feature is integrated directly into the recent threats table using the **AI Report** action.

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
│ Dashboard APIs               │
│ File Analysis APIs           │
│ Threat Prediction APIs       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Member 3                     │
│ React AI Analytics Dashboard │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Security Analytics UI        │
│                              │
│ • Threat Analytics           │
│ • AI Threat Prediction      │
│ • Threat Score               │
│ • Threat Category            │
│ • Behavioral Findings        │
│ • Recommended Action         │
│ • Security Summary           │
└──────────────────────────────┘
