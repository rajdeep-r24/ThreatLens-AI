from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Any

from app.api.deps import get_db, get_current_user
from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User, RoleEnum, ROLE_PERMISSIONS
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
)

router = APIRouter(prefix="/auth", tags=["Authentication & RBAC"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user in the ThreatLens-AI system with a designated role.
    """
    # Check if email or username already exists
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists."
        )

    # Create new user
    new_user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=hash_password(user_in.password),
        role=user_in.role or RoleEnum.SECURITY_ANALYST,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user via email/username and password. Returns JWT access & refresh tokens.
    """
    # Find user by username OR email
    user = db.query(User).filter(
        (User.email == credentials.username_or_email) | (User.username == credentials.username_or_email)
    ).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials: username/email or password incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is currently inactive. Contact your administrator."
        )

    access_token = create_access_token(subject=user.id, role=user.role.value)
    refresh_token = create_refresh_token(subject=user.id, role=user.role.value)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=Dict[str, Any])
def refresh_token(
    token_in: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a new access token using a valid refresh token.
    """
    payload = decode_token(token_in.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    new_access_token = create_access_token(subject=user.id, role=user.role.value)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get profile details, role, and permissions of the currently authenticated user.
    """
    return current_user


@router.get("/roles-matrix", response_model=Dict[str, List[str]])
def get_roles_permission_matrix():
    """
    Public catalog of system roles and their assigned permissions in ThreatLens-AI.
    """
    return {role.value: perms for role, perms in ROLE_PERMISSIONS.items()}
