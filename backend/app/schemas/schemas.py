from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str
    role: str = "Security Analyst"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class YARAResultResponse(BaseModel):
    id: int
    file_id: int
    rule_name: str
    severity: str
    tags: Optional[List[str]] = []
    matched_strings: Optional[List[str]] = []
    matched_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisResultResponse(BaseModel):
    id: int
    file_id: int
    pe_headers: Optional[Any] = None
    extracted_strings: Optional[List[str]] = []
    suspicious_apis: Optional[List[str]] = []
    network_indicators: Optional[Any] = None
    risk_score: int
    threat_classification: Optional[str] = None
    recommended_action: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FileResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    filename: str
    file_path: str
    file_size: int
    md5_hash: Optional[str] = None
    sha256_hash: Optional[str] = None
    file_type: Optional[str] = None
    status: str
    uploaded_at: datetime
    analysis_result: Optional[AnalysisResultResponse] = None
    yara_results: Optional[List[YARAResultResponse]] = []

    model_config = ConfigDict(from_attributes=True)
