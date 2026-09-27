"""
ThreatLens AI - Milestone 3
Member 4: Notifications & Reporting Workflow

Creates security notifications from threat prediction results.
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
    Create a security notification based on threat assessment.
    """

    if threat_level == "Critical":
        severity = "Critical"
        notification_type = "Security Warning"
        message = (
            f"Critical threat detected in {filename}. "
            "Immediate investigation is recommended."
        )

    elif threat_level == "High":
        severity = "High"
        notification_type = "Threat Alert"
        message = (
            f"High-risk threat detected in {filename}. "
            "Further investigation is recommended."
        )

    elif threat_level == "Medium":
        severity = "Medium"
        notification_type = "Security Warning"
        message = (
            f"Suspicious activity detected in {filename}. "
            "Security review is recommended."
        )

    else:
        severity = "Low"
        notification_type = "Detection Status"
        message = (
            f"No significant threat detected in {filename}. "
            "File can be monitored."
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