"""
Database setup and session management.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wallet_app.db")

# Create engine - this connects to the database
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL (production)
    engine = create_engine(DATABASE_URL)
else:
    # SQLite (development)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )

# SessionLocal - factory to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base - all our database models will inherit from this
Base = declarative_base()


def get_db():
    """
    Get a database session.
    We'll use this in our routes to access the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
