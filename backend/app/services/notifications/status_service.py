"""
ThreatLens AI - Milestone 3
Member 4: Detection Status Updates
"""

from datetime import datetime, timezone
from typing import Any, Dict


def create_status_update(
    filename: str,
    status: str,
    message: str,
) -> Dict[str, Any]:
    """Create a detection status update."""

    return {
        "filename": filename,
        "status": status,
        "message": message,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }