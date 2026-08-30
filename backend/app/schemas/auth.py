from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.user import RoleEnum


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None


class UserRegister(UserBase):
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    role: Optional[RoleEnum] = RoleEnum.SECURITY_ANALYST


class UserLogin(BaseModel):
    # Allows logging in with either username or email
    username_or_email: str
    password: str


class UserResponse(UserBase):
    id: int
    role: RoleEnum
    permissions: List[str] = []
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
    role: RoleEnum
    type: str
    exp: int


class RoleUpdateRequest(BaseModel):
    user_id: int
    new_role: RoleEnum
