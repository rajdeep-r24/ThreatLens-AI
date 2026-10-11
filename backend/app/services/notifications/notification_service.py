"""
ThreatLens AI - Security Notifications Service
Generates contextual alert notifications based on threat analysis and risk scores.
"""

from datetime import datetime, timezone
from typing import Any, Dict


def create_notification(
    filename: str,
    threat_level: str,
    threat_category: str,
    threat_score: int,
    recommended_action: str,
) -> Dict[str, Any]:
    """
    Generate a structured security alert notification based on threat findings.
    """
    if threat_level == "Critical":
        severity = "Critical"
        notification_type = "Security Warning"
        message = (
            f"Critical severity threat detected in {filename}. "
            "Immediate host isolation and analyst triage recommended."
        )
    elif threat_level == "High":
        severity = "High"
        notification_type = "Threat Alert"
        message = (
            f"High-risk threat indicators detected in {filename}. "
            "Further forensic review and process monitoring recommended."
        )
    elif threat_level == "Medium":
        severity = "Medium"
        notification_type = "Security Warning"
        message = (
            f"Suspicious heuristic activity detected in {filename}. "
            "Behavioral verification recommended."
        )
    else:
        severity = "Low"
        notification_type = "Detection Status"
        message = (
            f"Clean / low-risk assessment for {filename}. "
            "Standard monitoring baseline applied."
        )

    return {
        "notification": {
            "type": notification_type,
            "severity": severity,
            "message": message,
        },
        "file": {
            "filename": filename,
        },
        "threat": {
            "level": threat_level,
            "category": threat_category,
            "score": threat_score,
        },
        "response": {
            "recommended_action": recommended_action,
        },
        "status": "Generated",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
