"""
Authentication tests for RosePay application.
"""
import pytest
from fastapi.testclient import TestClient

@pytest.mark.auth
@pytest.mark.unit
class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_register_user_success(self, client: TestClient, test_user_data):
        """Test successful user registration."""
        response = client.post("/api/v1/users/register", json=test_user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "id" in data
        assert "password" not in data  # Password should not be returned
    
    def test_register_duplicate_email_fails(self, client: TestClient, test_user_data):
        """Test registration with duplicate email fails."""
        # Register first user
        client.post("/api/v1/users/register", json=test_user_data)
        
        # Try to register same email again
        response = client.post("/api/v1/users/register", json=test_user_data)
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_invalid_email_fails(self, client: TestClient):
        """Test registration with invalid email fails."""
        invalid_data = {
            "email": "invalid-email",
            "password": "password123",
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/users/register", json=invalid_data)
        assert response.status_code == 422
    
    def test_register_short_password_fails(self, client: TestClient):
        """Test registration with short password fails."""
        invalid_data = {
            "email": "test@example.com",
            "password": "123",  # Too short
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/users/register", json=invalid_data)
        assert response.status_code == 422
    
    def test_register_missing_required_fields_fails(self, client: TestClient):
        """Test registration with missing required fields fails."""
        # Missing email
        response = client.post("/api/v1/users/register", json={
            "password": "password123",
            "full_name": "Test User"
        })
        assert response.status_code == 422
        
        # Missing password
        response = client.post("/api/v1/users/register", json={
            "email": "test@example.com",
            "full_name": "Test User"
        })
        assert response.status_code == 422

@pytest.mark.auth
@pytest.mark.unit
class TestUserLogin:
    """Test user login functionality."""
    
    def test_login_success(self, client: TestClient, test_user_data):
        """Test successful user login."""
        # Register user first
        client.post("/api/v1/users/register", json=test_user_data)
        
        # Login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/v1/users/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 10  # JWT token should be substantial
    
    def test_login_invalid_email_fails(self, client: TestClient):
        """Test login with invalid email fails."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        
        response = client.post("/api/v1/users/login", json=login_data)
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_invalid_password_fails(self, client: TestClient, test_user_data):
        """Test login with invalid password fails."""
        # Register user first
        client.post("/api/v1/users/register", json=test_user_data)
        
        # Try login with wrong password
        login_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/users/login", json=login_data)
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_missing_fields_fails(self, client: TestClient):
        """Test login with missing fields fails."""
        # Missing email
        response = client.post("/api/v1/users/login", json={
            "password": "password123"
        })
        assert response.status_code == 422
        
        # Missing password
        response = client.post("/api/v1/users/login", json={
            "email": "test@example.com"
        })
        assert response.status_code == 422

@pytest.mark.auth
@pytest.mark.unit
class TestTokenValidation:
    """Test JWT token validation."""
    
    def test_protected_endpoint_without_token_fails(self, client: TestClient):
        """Test accessing protected endpoint without token fails."""
        response = client.get("/api/v1/wallets")
        assert response.status_code == 401
    
    def test_protected_endpoint_with_invalid_token_fails(self, client: TestClient):
        """Test accessing protected endpoint with invalid token fails."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/wallets", headers=headers)
        assert response.status_code == 401
    
    def test_protected_endpoint_with_valid_token_succeeds(self, authenticated_client: TestClient):
        """Test accessing protected endpoint with valid token succeeds."""
        response = authenticated_client.get("/api/v1/wallets")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_token_format_validation(self, client: TestClient):
        """Test token format validation."""
        # No Bearer prefix
        headers = {"Authorization": "invalid_format_token"}
        response = client.get("/api/v1/wallets", headers=headers)
        assert response.status_code == 401
        
        # Empty token
        headers = {"Authorization": "Bearer "}
        response = client.get("/api/v1/wallets", headers=headers)
        assert response.status_code == 401

@pytest.mark.auth
@pytest.mark.integration
class TestAuthIntegration:
    """Integration tests for authentication flow."""
    
    def test_complete_auth_flow(self, client: TestClient, test_user_data):
        """Test complete authentication flow: register -> login -> access protected resource."""
        # Step 1: Register
        register_response = client.post("/api/v1/users/register", json=test_user_data)
        assert register_response.status_code == 201
        
        # Step 2: Login
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 3: Access protected resource
        wallets_response = client.get("/api/v1/wallets", headers=headers)
        assert wallets_response.status_code == 200
        assert isinstance(wallets_response.json(), list)
    
    def test_multiple_users_isolation(self, client: TestClient, test_user_data, test_user_data_2):
        """Test that users cannot access each other's data."""
        # Register and login first user
        client.post("/api/v1/users/register", json=test_user_data)
        login1 = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token1 = login1.json()["access_token"]
        
        # Register and login second user
        client.post("/api/v1/users/register", json=test_user_data_2)
        login2 = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token2 = login2.json()["access_token"]
        
        # Create wallet for user 1
        headers1 = {"Authorization": f"Bearer {token1}"}
        wallet1_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers1)
        assert wallet1_response.status_code == 201
        
        # User 2 should not see user 1's wallet
        headers2 = {"Authorization": f"Bearer {token2}"}
        wallets2_response = client.get("/api/v1/wallets", headers=headers2)
        assert wallets2_response.status_code == 200
        assert len(wallets2_response.json()) == 0  # User 2 has no wallets
