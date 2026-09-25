ThreatLens-AI – AI Threat Analytics Dashboard










Team 2 | Member 3

Member: K. Vamshi
Role: AI Threat Analytics Dashboard Developer
Milestone: Week 3 – Milestone 3
Branch: feat/ai-analytics-dashboard
Status: Completed

📌 Overview

As part of Team 2's ThreatLens-AI project, I worked on the AI Threat Analytics Dashboard during Week 3 / Milestone 3.

Building on the monitoring dashboard work from the previous milestone, I integrated the dashboard with the AI threat prediction workflow and completed the frontend-to-backend flow for generating and displaying AI-based threat reports for analyzed files.

The main goal of this milestone was to provide security analysts with a deeper view of individual file threats through AI-generated analysis in addition to the existing static-analysis results.

👨‍💻 My Contribution

AI Threat Analytics & Reporting

I extended the existing React dashboard and implemented the following Week 3 features:

Integrated the AI threat prediction report workflow into the dashboard

Added an AI Report action for analyzed files

Added an AI Threat Prediction Report modal

Displayed AI-generated threat level and final threat score

Displayed AI threat category and recommended action

Displayed behavioral analysis findings with severity and descriptions

Added AI security summary output

Connected the frontend to the threat prediction report API

Added loading-state handling for AI report generation

Added error handling so the report view does not remain stuck when an API call fails

Fixed the frontend import/integration issue for the AI report API function

Resolved the Vite frontend-to-FastAPI proxy connection issue

Verified dashboard and AI report API communication through browser Network tools

🤖 AI Threat Report Features

1. AI Report Generation

Each analyzed file can be opened through the AI Report action from the Recent Threats table.

The dashboard requests the corresponding AI prediction report from the backend.

API used:

GET /api/v1/predictions/{file_id}/report

2. Threat Assessment

The AI report displays:

Threat Level

Final Threat Score

Threat Category

This gives analysts an additional AI-based interpretation of the static-analysis results.

3. Recommended Action

The report displays a recommended security action based on the generated threat assessment.

Example:

Flag for security review

4. Behavioral Findings

The dashboard displays individual behavioral findings returned by the AI report, including:

Behavior name

Severity

Description

This makes the generated security reasoning easier to inspect at the file level.

5. Security Summary

The AI report also displays a concise security summary for the selected file so analysts can quickly understand the overall assessment without reviewing every finding individually.

🔧 API Integration & Fixes

Dashboard APIs

Verified the existing dashboard endpoints:

GET /api/v1/dashboard/stats   → 200 OK
GET /api/v1/files             → 200 OK

AI Prediction API

Integrated the AI prediction report endpoint:

GET /api/v1/predictions/{file_id}/report

Frontend Proxy Fix

Resolved the local Vite proxy connection problem by routing API requests to the IPv4 loopback address:

target: 'http://127.0.0.1:8000'

instead of:

target: 'http://localhost:8000'

This resolved the frontend proxy timeout seen during local testing.

🔄 AI Report Data Flow

┌──────────────────────────────┐
│ User selects a scanned file  │
│ and clicks "AI Report"       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ React Dashboard              │
│ handleViewAiReport()         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Frontend API Service         │
│ fetchThreatPredictionReport  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Vite API Proxy               │
│ /api → 127.0.0.1:8000       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ FastAPI Backend              │
│ /predictions/{id}/report     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ AI Threat Prediction Result  │
│                              │
│ • Threat Level               │
│ • Threat Score               │
│ • Threat Category            │
│ • Recommended Action         │
│ • Behavioral Findings        │
│ • Security Summary           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ AI Threat Prediction Report  │
│ displayed in React modal     │
└──────────────────────────────┘

🧪 Testing & Validation

The Week 3 implementation was validated locally using the running React and FastAPI applications.

Verified

Dashboard statistics API returns successful responses

File listing API returns successful responses

AI Report button opens the report modal

AI prediction report request reaches the backend

AI report response is rendered in the dashboard

Loading state is cleared after the request completes

Frontend/backend proxy communication works through Vite

Browser Network tab confirms successful API communication

Example validated flow

Dashboard load
     ↓
/api/v1/dashboard/stats   → 200 OK
/api/v1/files             → 200 OK
     ↓
AI Report clicked
     ↓
/api/v1/predictions/{file_id}/report
     ↓
AI report displayed successfully

🛠 Technology Used

React — dashboard UI and components

Vite — frontend development server and API proxy

JavaScript (ES6) — dashboard logic and API integration

Recharts — data visualization from the dashboard milestone

Lucide React — dashboard and security icons

FastAPI — backend API integration

Python — backend ecosystem and threat-analysis services

Git & GitHub — version control and team collaboration

📂 Main Frontend Changes

Key files updated during Week 3:

frontend/src/pages/DashboardPage.jsx
frontend/src/services/api.js
frontend/vite.config.js

DashboardPage.jsx

Added AI Report interaction

Added AI report modal rendering

Added threat assessment display

Added behavioral findings display

Added loading and error-state handling

api.js

Integrated fetchThreatPredictionReport(fileId)

Connected the dashboard to the AI prediction report endpoint

vite.config.js

Updated the API proxy target for reliable local frontend-to-backend communication

📌 Milestone 3 Result

The Week 3 milestone extends the ThreatLens-AI dashboard from basic threat monitoring into AI-assisted threat analysis.

The dashboard now allows an analyst to select an analyzed file and view an AI-generated threat prediction report containing assessment, score, category, recommended action, behavioral findings, and a security summary.

🚀 Future Enhancements

Add AI report history and comparison between scans

Add export/download of AI threat reports

Add analyst feedback on AI predictions

Add trend analytics for AI-generated threat scores

Add deeper correlation between YARA findings and AI assessments

👤 Member

K. Vamshi
Team 2 – Member 3
Role: AI Threat Analytics Dashboard Developer
Week 3 / Milestone 3
Branch: feat/ai-analytics-dashboard
