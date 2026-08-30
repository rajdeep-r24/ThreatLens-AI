import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.api.deps import get_db, get_current_user
from app.models.scan import File, AnalysisResult, YARAResult
from app.models.user import User
from app.schemas.scan import FileResponse, DashboardStatsResponse
from app.services.static_analysis import run_static_analysis_pipeline

router = APIRouter(tags=["File Analysis & Dashboard Stats"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/files/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_and_analyze_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db)
):
    """
    Upload a suspicious binary or document sample and execute the static analysis pipeline.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected for upload.")

    safe_filename = os.path.basename(file.filename)
    file_destination = os.path.join(UPLOAD_DIR, safe_filename)

    # Save file to uploads quarantine folder
    with open(file_destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Run unified static analysis pipeline
        analysis_data = run_static_analysis_pipeline(file_destination)

        # Create File record in database
        file_record = File(
            filename=safe_filename,
            file_path=file_destination,
            file_size=analysis_data["file_size"],
            md5_hash=analysis_data["md5_hash"],
            sha256_hash=analysis_data["sha256_hash"],
            file_type=analysis_data["file_type"],
            status="completed",
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)

        # Create AnalysisResult record
        result_record = AnalysisResult(
            file_id=file_record.id,
            pe_headers=analysis_data.get("pe_headers"),
            extracted_strings=analysis_data.get("extracted_strings"),
            suspicious_apis=analysis_data.get("suspicious_apis"),
            network_indicators=analysis_data.get("network_indicators"),
            risk_score=analysis_data["risk_score"],
            threat_classification=analysis_data["threat_classification"],
            recommended_action=analysis_data["recommended_action"],
        )
        db.add(result_record)
        db.commit()
        db.refresh(file_record)

        return file_record

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Static analysis scan failed: {str(e)}"
        )


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
