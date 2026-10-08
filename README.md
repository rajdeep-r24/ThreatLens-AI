# ThreatLens-AI – Dual-Engine Threat Intelligence Platform

![React](https://img.shields.io/badge/React-frontend-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-backend%20API-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![Status](https://img.shields.io/badge/status-completed-brightgreen)

## 📌 Overview

**ThreatLens-AI** is a professional, Dual-Engine Threat Intelligence Platform built for Security Operations Centers (SOC). It provides real-time malware analysis, threat monitoring, and actionable intelligence to security analysts.

By combining traditional static analysis with advanced machine learning, ThreatLens-AI can accurately detect both known malware signatures and zero-day threats through behavioral prediction.

---

## 🚀 Key Features

### 1. Dual-Engine Analysis
- **Static & Heuristic Analysis:** Instantly extracts PE headers, strings, network indicators, and calculates hashes. Utilizes custom **YARA rules** to identify known malicious byte patterns.
- **Machine Learning Prediction:** Employs a **Random Forest Classifier** trained on the ClaMP dataset to analyze file features and predict malicious behavior, catching zero-day threats that evade static signatures.

### 2. Threat Monitoring Dashboard
An interactive, real-time dashboard providing security analysts with a clear view of:
- Total Scans and Threat Detections
- Malware Classification Distribution
- Risk Level Categorization (Low, Medium, High, Critical)
- Recent Threat Telemetry

### 3. Detailed Intelligence Reports
- Comprehensive breakdown of triggered YARA rules.
- AI Confidence Scores and behavioral capability mappings.
- Recommended mitigation actions for SOC teams.

### 4. Professional UI/UX
- Fully responsive interface built with React and Tailwind CSS.
- Synchronized Light/Dark mode for analyst comfort.
- Real-time data visualization using Recharts.

---

## 🛠️ Technology Stack

- **Frontend:** React, Vite, Tailwind CSS, Recharts
- **Backend:** FastAPI, Python (Scikit-Learn, Joblib)
- **Database:** SQLite / SQLAlchemy

---

## ⚙️ Running Locally

1. **Backend Setup:**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access the Application:**
   Open your browser and navigate to `http://localhost:5173` (or the port provided by Vite).
