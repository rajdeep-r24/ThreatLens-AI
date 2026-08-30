from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RoleEnum(str, Enum):
    ADMINISTRATOR = "Administrator"
    SECURITY_ANALYST = "Security Analyst"
    SOC_TEAM = "SOC Team Member"
    RESEARCHER = "Researcher"


# Permission catalog according to ThreatLens-AI specifications
ROLE_PERMISSIONS: Dict[RoleEnum, List[str]] = {
    RoleEnum.ADMINISTRATOR: [
        "user:manage",
        "platform:settings",
        "integrations:manage",
        "dashboards:view_all",
        "platform:monitor",
        "policies:manage",
        "file:upload",
        "scan:static",
        "report:view_malware",
        "dashboard:threat_monitor",
        "alert:review",
        "logs:monitor",
        "threats:view_active",
        "incidents:track",
        "datasets:access",
        "families:analyze",
    ],
    RoleEnum.SECURITY_ANALYST: [
        "file:upload",
        "scan:static",
        "report:view_malware",
        "dashboard:threat_monitor",
        "alert:review",
        "report:investigation",
    ],
    RoleEnum.SOC_TEAM: [
        "logs:monitor",
        "threats:view_active",
        "dashboard:security",
        "incidents:track",
        "alert:review_history",
        "report:operational",
    ],
    RoleEnum.RESEARCHER: [
        "samples:upload_research",
        "datasets:access",
        "families:analyze",
        "results:review",
        "report:export",
        "analytics:historical",
    ],
}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.SECURITY_ANALYST, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    @property
    def permissions(self) -> List[str]:
        return ROLE_PERMISSIONS.get(self.role, [])
