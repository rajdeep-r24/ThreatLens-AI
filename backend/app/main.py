import os
import sys
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.db.database import get_db, Base, engine
from backend.app.models.models import User, File, AnalysisResult, YARAResult
from backend.app.schemas.schemas import UserResponse, UserCreate, FileResponse, AnalysisResultResponse, YARAResultResponse
from backend.app.db.init_db import init_db

app = FastAPI(
    title="ThreatLens AI Backend API",
    description="AI-Powered Malware Classification & Threat Detection System API (Milestone 1 Backbone)",
    version="1.0.0"
)

# Enable CORS for React Frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    # Initialize DB tables and seed initial demo data
    init_db()


@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "system": "ThreatLens AI System Core",
        "milestone": 1,
        "database": "connected"
    }


# ================= USER MANAGEMENT (Member 1 Schema & Member 3 Auth prep) =================

@app.get("/api/users", response_model=List[UserResponse], tags=["User Management"])
def get_users(db: Session = Depends(get_db)):
    """Retrieve list of registered users and their security roles."""
    return db.query(User).all()


@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["User Management"])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account."""
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=f"hashed_{user_in.password}", # Mock hashing for milestone 1 baseline
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ================= FILE ANALYSIS & YARA RESULTS (Member 1 Models & Member 2 UI) =================

@app.get("/api/files", response_model=List[FileResponse], tags=["File Analysis"])
def list_files(db: Session = Depends(get_db)):
    """List all analyzed files with static analysis and YARA match summary."""
    return db.query(File).order_by(File.uploaded_at.desc()).all()


@app.get("/api/files/{file_id}", response_model=FileResponse, tags=["File Analysis"])
def get_file_details(file_id: int, db: Session = Depends(get_db)):
    """Get complete static analysis and YARA details for a specific file."""
    file_record = db.query(File).filter(File.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File record not found")
    return file_record


@app.get("/api/dashboard/stats", tags=["Dashboard"])
def get_dashboard_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Provide aggregated security statistics for Member 2 UI Dashboard."""
    total_files = db.query(File).count()
    completed_scans = db.query(File).filter(File.status == "completed").count()
    
    # High risk files (Risk score >= 60)
    high_risk_count = db.query(AnalysisResult).filter(AnalysisResult.risk_score >= 60).count()
    
    # Total YARA detections
    yara_detections = db.query(YARAResult).count()
    
    # Calculate average risk score
    all_scores = [r.risk_score for r in db.query(AnalysisResult).all()]
    avg_risk_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0.0

    return {
        "total_scans": total_files,
        "completed_scans": completed_scans,
        "malicious_threats": high_risk_count,
        "yara_matches": yara_detections,
        "avg_risk_score": avg_risk_score,
        "system_status": "Operational",
        "active_rules": 48
    }
