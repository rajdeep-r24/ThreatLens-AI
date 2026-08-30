from app.schemas.auth import (
    UserBase,
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
)
from app.schemas.scan import (
    FileResponse,
    AnalysisResultResponse,
    YARAResultResponse,
    DashboardStatsResponse,
)

UserCreate = UserRegister

__all__ = [
    "UserBase",
    "UserCreate",
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
    "RefreshTokenRequest",
    "FileResponse",
    "AnalysisResultResponse",
    "YARAResultResponse",
    "DashboardStatsResponse",
]
