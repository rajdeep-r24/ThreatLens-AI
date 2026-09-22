from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.api.deps import get_db, get_current_user
from app.models.scan import File, AnalysisResult
from app.services.behavioral_analysis.behavioral_analysis import analyze_behavior
from app.services.behavioral_analysis.threat_prediction import predict_threat
from app.services.behavioral_analysis.threat_report import generate_threat_report
from app.services.notifications.notification_service import create_notification
from app.services.notifications.status_service import create_status_update

router = APIRouter(tags=["AI Prediction & Threat Reports"])


@router.get("/predictions/{file_id}/report", response_model=Dict[str, Any])
async def get_threat_prediction_report(
    file_id: int,
    db: Session = Depends(get_db),
    # Uncomment the below line to require authentication
    # current_user = Depends(get_current_user)
):
    """
    Generate an AI Threat Prediction Report for a specific file.
    Uses Member 1's AI Prediction & Behavioral Analysis logic.
    """
    
    # 1. Fetch the File and Analysis Result
    file_record = db.query(File).filter(File.id == file_id).first()
    
    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
        
    analysis = file_record.analysis_result
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis results not found for this file. Has it been scanned?"
        )
        
    # 2. Extract Static Indicators for Behavioral Analysis
    suspicious_apis = analysis.suspicious_apis or []
    extracted_strings = analysis.extracted_strings or []
    network_indicators = analysis.network_indicators or {}
    pe_headers = analysis.pe_headers or {}
    
    # Format YARA results for the behavioral analysis function
    yara_list = [
        {
            "rule_name": yr.rule_name,
            "severity": yr.severity,
            "tags": yr.tags,
            "matched_strings": yr.matched_strings
        }
        for yr in file_record.yara_results
    ]
    
    # 3. Step 1: Behavioral Analysis (Member 1 logic)
    behavioral_result = analyze_behavior(
        suspicious_apis=suspicious_apis,
        extracted_strings=extracted_strings,
        network_indicators=network_indicators,
        pe_headers=pe_headers,
        yara_results=yara_list
    )
    
    # 4. Step 2: Threat Prediction (Fusion of ML + Behavior)
    ml_prediction = analysis.ml_prediction or "Unknown"
    ml_confidence = analysis.ml_confidence or 0.0
    
    threat_prediction = predict_threat(
        ml_prediction=ml_prediction,
        ml_confidence=ml_confidence,
        behavioral_result=behavioral_result
    )
    
    # 5. Step 3: Generate the Final Threat Report
    report = generate_threat_report(
        filename=file_record.filename,
        sha256_hash=file_record.sha256_hash or "Unknown",
        threat_prediction=threat_prediction
    )

    # 6. Create Member 4 notification
    notification = create_notification(
        filename=file_record.filename,
        threat_level=threat_prediction.get("threat_level", "Unknown"),
        threat_category=threat_prediction.get(
            "threat_category",
            "Unknown"
        ),
        threat_score=threat_prediction.get(
            "final_threat_score",
            0
        ),
        recommended_action=threat_prediction.get(
            "recommended_action",
            "Review manually"
        ),
    )

    # 7. Create detection status update
    status_update = create_status_update(
        filename=file_record.filename,
        status="Completed",
        message="Threat analysis and prediction completed successfully.",
    )

    return {
        "threat_report": report,
        "notification": notification,
        "status_update": status_update,
    }