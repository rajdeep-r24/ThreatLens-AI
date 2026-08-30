from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.api.deps import require_roles, require_permissions
from app.models.user import User, RoleEnum

router = APIRouter(tags=["Role-Restricted Workflows (RBAC Demo)"])


@router.get("/admin/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_roles([RoleEnum.ADMINISTRATOR]))
) -> Dict[str, Any]:
    """
    Administrator-only endpoint for managing users, settings, and policies.
    """
    return {
        "status": "success",
        "message": "Welcome to Administrator Management Console.",
        "user": current_user.username,
        "role": current_user.role.value,
        "capabilities": [
            "User & Role Management",
            "Platform Configuration",
            "API & SIEM Integrations",
            "Security Policy Enforcement"
        ]
    }


@router.get("/analyst/scans")
def analyst_scan_center(
    current_user: User = Depends(require_roles([RoleEnum.SECURITY_ANALYST, RoleEnum.ADMINISTRATOR]))
) -> Dict[str, Any]:
    """
    Security Analyst endpoint for submitting suspicious files and running static scans.
    """
    return {
        "status": "success",
        "message": "Static Analysis & Scan Queue Access Granted.",
        "user": current_user.username,
        "role": current_user.role.value,
        "capabilities": [
            "Upload Suspicious Files",
            "Run Static Analysis",
            "Generate Investigation Reports",
            "Review Malware Signatures"
        ]
    }


@router.get("/soc/threat-feed")
def soc_monitoring_center(
    current_user: User = Depends(require_roles([RoleEnum.SOC_TEAM, RoleEnum.ADMINISTRATOR]))
) -> Dict[str, Any]:
    """
    SOC Team Member endpoint for real-time detection logs and incident tracking.
    """
    return {
        "status": "success",
        "message": "SOC Threat Feed & Real-Time Monitoring Access Granted.",
        "user": current_user.username,
        "role": current_user.role.value,
        "capabilities": [
            "Monitor Detection Logs",
            "Track Active Malware Incidents",
            "Review Alert History",
            "Generate Operational Reports"
        ]
    }


@router.get("/researcher/samples")
def researcher_workspace(
    current_user: User = Depends(require_roles([RoleEnum.RESEARCHER, RoleEnum.ADMINISTRATOR]))
) -> Dict[str, Any]:
    """
    Researcher endpoint for uploading malware samples, dataset access, and family analysis.
    """
    return {
        "status": "success",
        "message": "Malware Research Workspace Access Granted.",
        "user": current_user.username,
        "role": current_user.role.value,
        "capabilities": [
            "Upload Malware Samples for Research",
            "Access Malware Datasets",
            "Analyze Malware Families",
            "Historical Threat Analytics"
        ]
    }


@router.get("/audit/logs")
def audit_logs_permission_check(
    current_user: User = Depends(require_permissions(["logs:monitor"]))
) -> Dict[str, Any]:
    """
    Endpoint protected via granular permission: 'logs:monitor'
    """
    return {
        "status": "success",
        "message": "Access granted via granular permission 'logs:monitor'",
        "user": current_user.username,
        "role": current_user.role.value
    }
