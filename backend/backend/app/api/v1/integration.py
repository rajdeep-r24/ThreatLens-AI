"""
ThreatLens AI - Milestone 3
Member 5: Integration & Security/Threat Reports

Connects Members 1-4 into one complete Milestone 3 workflow.
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.scan import File

from app.services.behavioral_analysis.behavioral_analysis import (
    analyze_behavior
)

from app.services.behavioral_analysis.threat_prediction import (
    predict_threat
)

from app.services.behavioral_analysis.threat_report import (
    generate_threat_report
)

from app.services.notifications.notification_service import (
    create_notification
)

from app.services.notifications.status_service import (
    create_status_update
)


router = APIRouter(
    prefix="/integration",
    tags=["Milestone 3 Integration"]
)


@router.get(
    "/files/{file_id}/complete-report",
    response_model=Dict[str, Any]
)
async def generate_complete_security_report(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    Execute the complete Milestone 3 workflow.

    Member 5 integrates:
        Member 1 -> Behavioral Analysis & Threat Prediction
        Member 2 -> Prediction API / Reports
        Member 3 -> Analytics data
        Member 4 -> Notifications & Status
    """

    # ---------------------------------------------------------
    # 1. GET FILE
    # ---------------------------------------------------------

    file_record = (
        db.query(File)
        .filter(File.id == file_id)
        .first()
    )

    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # ---------------------------------------------------------
    # 2. GET EXISTING ANALYSIS
    # ---------------------------------------------------------

    analysis = file_record.analysis_result

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Analysis results not found. "
                "Run file analysis before generating "
                "the final security report."
            )
        )

    # ---------------------------------------------------------
    # 3. PREPARE MEMBER 1 INPUT
    # ---------------------------------------------------------

    suspicious_apis = (
        analysis.suspicious_apis or []
    )

    extracted_strings = (
        analysis.extracted_strings or []
    )

    network_indicators = (
        analysis.network_indicators or {}
    )

    pe_headers = (
        analysis.pe_headers or {}
    )

    yara_results = [
        {
            "rule_name": result.rule_name,
            "severity": result.severity,
            "tags": result.tags or [],
            "matched_strings": result.matched_strings or []
        }
        for result in file_record.yara_results
    ]

    # ---------------------------------------------------------
    # 4. MEMBER 1 - BEHAVIORAL ANALYSIS
    # ---------------------------------------------------------

    behavioral_result = analyze_behavior(
        suspicious_apis=suspicious_apis,
        extracted_strings=extracted_strings,
        network_indicators=network_indicators,
        pe_headers=pe_headers,
        yara_results=yara_results
    )

    # ---------------------------------------------------------
    # 5. MEMBER 1 - THREAT PREDICTION
    # ---------------------------------------------------------

    ml_prediction = (
        analysis.ml_prediction or "Unknown"
    )

    ml_confidence = (
        analysis.ml_confidence or 0.0
    )

    threat_prediction = predict_threat(
        ml_prediction=ml_prediction,
        ml_confidence=ml_confidence,
        behavioral_result=behavioral_result
    )

    # ---------------------------------------------------------
    # 6. MEMBER 2 - THREAT REPORT
    # ---------------------------------------------------------

    threat_report = generate_threat_report(
        filename=file_record.filename,
        sha256_hash=(
            file_record.sha256_hash or "Unknown"
        ),
        threat_prediction=threat_prediction
    )

    # ---------------------------------------------------------
    # 7. MEMBER 4 - SECURITY NOTIFICATION
    # ---------------------------------------------------------

    notification = create_notification(
        filename=file_record.filename,
        threat_level=threat_prediction.get(
            "threat_level",
            "Unknown"
        ),
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
        )
    )

    # ---------------------------------------------------------
    # 8. MEMBER 4 - STATUS UPDATE
    # ---------------------------------------------------------

    status_update = create_status_update(
        filename=file_record.filename,
        status="Completed",
        message=(
            "Complete Milestone 3 security workflow "
            "completed successfully."
        )
    )

    # ---------------------------------------------------------
    # 9. FINAL MEMBER 5 RESPONSE
    # ---------------------------------------------------------

    return {
        "integration": {
            "milestone": "Milestone 3",
            "member": "Member 5",
            "status": "Completed",
            "workflow": [
                "File Analysis",
                "Behavioral Analysis",
                "Threat Prediction",
                "Threat Report",
                "Security Notification",
                "Status Update"
            ]
        },

        "file": {
            "id": file_record.id,
            "filename": file_record.filename,
            "sha256_hash": file_record.sha256_hash
        },

        "behavioral_analysis": behavioral_result,

        "threat_prediction": threat_prediction,

        "threat_report": threat_report,

        "notification": notification,

        "status_update": status_update
    }