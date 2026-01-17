"""
Pytest configuration and fixtures for RosePay tests.
"""
import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db, Base
from config import settings

# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test_wallet_app.db"

@pytest.fixture(scope="function")
def test_db():
    """Create a test database."""
    # Create test database engine
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal
    
    # Clean up - drop all tables
    Base.metadata.drop_all(bind=engine)
    
    # Remove test database file
    if os.path.exists("test_wallet_app.db"):
        os.remove("test_wallet_app.db")

@pytest.fixture
def db_session(test_db):
    """Create a database session for testing."""
    session = test_db()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(test_db):
    """Create a test client with test database."""
    # Override the get_db dependency
    def override_get_db():
        try:
            yield test_db()
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

@pytest.fixture
def test_user_data_2():
    """Second sample user data for testing."""
    return {
        "email": "test2@example.com",
        "password": "testpassword456",
        "full_name": "Test User 2"
    }

@pytest.fixture
def authenticated_client(client, test_user_data):
    """Create an authenticated client with a test user."""
    # Register user
    client.post("/api/v1/users/register", json=test_user_data)
    
    # Login to get token
    login_response = client.post("/api/v1/users/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    
    token = login_response.json()["access_token"]
    
    # Create authenticated client
    authenticated = TestClient(app)
    authenticated.headers.update({"Authorization": f"Bearer {token}"})
    
    return authenticated

@pytest.fixture
def test_wallet_data():
    """Sample wallet data for testing."""
    return {
        "currency": "USD"
    }

@pytest.fixture
def test_transaction_data():
    """Sample transaction data for testing."""
    return {
        "amount": 100.0,
        "description": "Test transaction"
    }

@pytest.fixture
def test_payment_link_data():
    """Sample payment link data for testing."""
    return {
        "amount": 50.0,
        "description": "Test payment link",
        "expires_hours": 24
    }

@pytest.fixture
def test_payment_request_data():
    """Sample payment request data for testing."""
    return {
        "recipient_email": "test2@example.com",
        "amount": 25.0,
        "description": "Test payment request"
    }
