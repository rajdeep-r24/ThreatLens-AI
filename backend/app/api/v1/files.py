from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.api.deps import get_db, get_current_user
from app.models.scan import File, AnalysisResult, YARAResult
from app.models.user import User
from app.schemas.scan import FileResponse, DashboardStatsResponse

router = APIRouter(tags=["File Analysis & Dashboard Stats"])


@router.get("/files", response_model=List[FileResponse])
def list_files(db: Session = Depends(get_db)):
    """List all analyzed files with static analysis and YARA match summary."""
    return db.query(File).order_by(File.uploaded_at.desc()).all()


@router.get("/files/{file_id}", response_model=FileResponse)
def get_file_details(file_id: int, db: Session = Depends(get_db)):
    """Get complete static analysis and YARA details for a specific file."""
    file_record = db.query(File).filter(File.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File record not found")
    return file_record


@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Provide aggregated security statistics for UI Dashboard."""
    total_files = db.query(File).count()
    completed_scans = db.query(File).filter(File.status == "completed").count()
    
    # High risk files (Risk score >= 60)
    high_risk_count = db.query(AnalysisResult).filter(AnalysisResult.risk_score >= 60).count()
    
    # Total YARA detections
    yara_detections = db.query(YARAResult).count()
    
    # Calculate average risk score
    all_scores = [r.risk_score for r in db.query(AnalysisResult).all()]
    avg_risk_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0.0

    return DashboardStatsResponse(
        total_scans=total_files,
        completed_scans=completed_scans,
        malicious_threats=high_risk_count,
        yara_matches=yara_detections,
        avg_risk_score=avg_risk_score,
        system_status="Operational",
        active_rules=48
    )
