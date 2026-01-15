"""
User routes - registration and login endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from schemas import UserCreate, UserResponse, UserLogin, Token
from services.user_service import create_user, authenticate_user
from core.security import create_access_token
from config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, summary="Register new user")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    WHAT IT DOES:
    1. Takes email, password, and optional name
    2. Creates user account
    3. Returns user info (without password)
    """
    return create_user(db, user)


@router.post("/login", response_model=Token, summary="Login user")
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login and get authentication token.
    
    WHAT IT DOES:
    1. Takes email and password
    2. Verifies credentials
    3. Returns JWT token for authentication
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": bool(user.is_active),
            "created_at": user.created_at.isoformat()
        }
    }
