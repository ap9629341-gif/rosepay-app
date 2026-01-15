"""
User service - handles user registration and authentication.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import User
from schemas import UserCreate
from core.security import get_password_hash, verify_password, create_access_token


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user account.
    
    WHAT IT DOES:
    1. Check if email already exists
    2. Hash the password (never store plain passwords!)
    3. Create user in database
    4. Return the new user
    """
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password before storing
    hashed_password = get_password_hash(user.password)
    
    # Create new user
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate user (login).
    
    WHAT IT DOES:
    1. Find user by email
    2. Verify password
    3. Return user if correct, None if wrong
    """
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
