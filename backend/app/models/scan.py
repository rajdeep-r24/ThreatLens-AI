from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON , Float
from sqlalchemy.orm import relationship

from app.models.user import Base, User


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # size in bytes
    md5_hash = Column(String(32), nullable=True, index=True)
    sha256_hash = Column(String(64), nullable=True, index=True)
    file_type = Column(String(100), nullable=True)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    uploader = relationship("User", back_populates="files")
    analysis_result = relationship("AnalysisResult", back_populates="file", uselist=False, cascade="all, delete-orphan")
    yara_results = relationship("YARAResult", back_populates="file", cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"), nullable=False, unique=True)
    pe_headers = Column(JSON, nullable=True)
    extracted_strings = Column(JSON, nullable=True)
    suspicious_apis = Column(JSON, nullable=True)
    network_indicators = Column(JSON, nullable=True)
    risk_score = Column(Integer, default=0)
    threat_classification = Column(String(100), nullable=True)
    recommended_action = Column(String(255), nullable=True)

    ml_prediction = Column(String(50), nullable=True)
    ml_confidence = Column(Float, nullable=True)
    final_risk_score = Column(Integer, default=0)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    file = relationship("File", back_populates="analysis_result")


class YARAResult(Base):
    __tablename__ = "yara_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    rule_name = Column(String(100), nullable=False)
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    tags = Column(JSON, nullable=True)
    matched_strings = Column(JSON, nullable=True)
    matched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    file = relationship("File", back_populates="yara_results")


# Link relationships to User model
User.files = relationship("File", back_populates="uploader", cascade="all, delete-orphan")
