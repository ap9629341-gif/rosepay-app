"""
Error handling and validation tests for RosePay application.
"""
import pytest
from fastapi.testclient import TestClient

@pytest.mark.unit
class TestValidationErrors:
    """Test input validation and error responses."""
    
    def test_invalid_json_format(self, authenticated_client: TestClient):
        """Test handling of invalid JSON format."""
        response = authenticated_client.post(
            "/api/v1/wallets",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_missing_required_fields_various_endpoints(self, authenticated_client: TestClient):
        """Test missing required fields across different endpoints."""
        # Wallet creation missing currency
        response = authenticated_client.post("/api/v1/wallets", json={})
        assert response.status_code == 422
        
        # Add money missing amount and description
        response = authenticated_client.post("/api/v1/wallets/1/add-money", json={})
        assert response.status_code == 422
        
        # Transfer missing recipient_user_id, amount, description
        response = authenticated_client.post("/api/v1/wallets/1/transfer", json={})
        assert response.status_code == 422
        
        # Payment link missing amount, description, expires_hours
        response = authenticated_client.post("/api/v1/payments/link/create", json={})
        assert response.status_code == 422
        
        # Payment request missing recipient_email, amount, description
        response = authenticated_client.post("/api/v1/payments/request", json={})
        assert response.status_code == 422
    
    def test_invalid_data_types(self, authenticated_client: TestClient):
        """Test handling of invalid data types."""
        # Wallet with non-string currency
        response = authenticated_client.post("/api/v1/wallets", json={"currency": 123})
        assert response.status_code == 422
        
        # Add money with string amount
        response = authenticated_client.post("/api/v1/wallets/1/add-money", json={
            "amount": "not_a_number",
            "description": "Invalid type"
        })
        assert response.status_code == 422
        
        # Transfer with string recipient_user_id
        response = authenticated_client.post("/api/v1/wallets/1/transfer", json={
            "recipient_user_id": "not_a_number",
            "amount": 50.0,
            "description": "Invalid type"
        })
        assert response.status_code == 422
    
    def test_extra_fields_ignored(self, authenticated_client: TestClient):
        """Test that extra fields in JSON are ignored."""
        response = authenticated_client.post("/api/v1/wallets", json={
            "currency": "USD",
            "extra_field": "should_be_ignored",
            "another_extra": 123
        })
        
        # Should succeed despite extra fields
        assert response.status_code == 201
        assert "extra_field" not in response.json()
        assert "another_extra" not in response.json()

@pytest.mark.unit
class TestBusinessLogicErrors:
    """Test business logic error handling."""
    
    def test_duplicate_email_registration(self, client: TestClient, test_user_data):
        """Test duplicate email registration error."""
        # Register first user
        client.post("/api/v1/users/register", json=test_user_data)
        
        # Try to register same email again
        response = client.post("/api/v1/users/register", json=test_user_data)
        
        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert "already registered" in error_detail.lower()
        assert "email" in error_detail.lower()
    
    def test_invalid_credentials_login(self, client: TestClient, test_user_data):
        """Test invalid credentials login error."""
        # Register user first
        client.post("/api/v1/users/register", json=test_user_data)
        
        # Try login with wrong password
        response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": "wrong_password"
        })
        
        assert response.status_code == 401
        error_detail = response.json()["detail"]
        assert "incorrect" in error_detail.lower()
    
    def test_nonexistent_resource_errors(self, authenticated_client: TestClient):
        """Test errors for non-existent resources."""
        # Non-existent wallet
        response = authenticated_client.get("/api/v1/wallets/99999")
        assert response.status_code == 404
        
        response = authenticated_client.get("/api/v1/wallets/99999/balance")
        assert response.status_code == 404
        
        # Non-existent transaction
        response = authenticated_client.get("/api/v1/transactions/99999")
        assert response.status_code == 404
        
        # Non-existent payment link
        response = authenticated_client.get("/api/v1/payments/link/nonexistent")
        assert response.status_code == 404
    
    def test_insufficient_funds_errors(self, authenticated_client: TestClient):
        """Test insufficient funds error handling."""
        # Create wallet with small balance
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 10.0,
            "description": "Small balance"
        })
        
        # Try to transfer more than available
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/transfer", json={
            "recipient_user_id": 999,
            "amount": 50.0,
            "description": "Too much transfer"
        })
        
        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert "insufficient" in error_detail.lower()
        assert "funds" in error_detail.lower()
    
    def test_self_transfer_error(self, authenticated_client: TestClient):
        """Test self-transfer error handling."""
        # Create wallet
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        user_id = wallet_response.json()["user_id"]
        
        # Try to transfer to self
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/transfer", json={
            "recipient_user_id": user_id,
            "amount": 25.0,
            "description": "Self transfer"
        })
        
        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert "yourself" in error_detail.lower()

@pytest.mark.unit
class TestAuthenticationErrors:
    """Test authentication and authorization errors."""
    
    def test_missing_token_error(self, client: TestClient):
        """Test error when no token provided."""
        endpoints = [
            "/api/v1/wallets",
            "/api/v1/transactions",
            "/api/v1/wallets/1",
            "/api/v1/wallets/1/balance",
            "/api/v1/wallets/1/add-money",
            "/api/v1/wallets/1/transfer",
            "/api/v1/payments/link/create",
            "/api/v1/payments/request",
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint) if endpoint.startswith("/api/v1/wallets/") or endpoint in ["/api/v1/wallets", "/api/v1/transactions"] else client.post(endpoint, json={})
            assert response.status_code == 401
    
    def test_invalid_token_error(self, client: TestClient):
        """Test error with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        
        endpoints = [
            "/api/v1/wallets",
            "/api/v1/transactions",
            "/api/v1/wallets/1",
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint, headers=headers)
            assert response.status_code == 401
    
    def test_malformed_token_error(self, client: TestClient):
        """Test error with malformed token."""
        test_cases = [
            {"Authorization": "InvalidFormat token"},
            {"Authorization": "Bearer"},
            {"Authorization": ""},
            {"Authorization": "Bearer "},
            {"Authorization": "bearer token"},  # lowercase
        ]
        
        for headers in test_cases:
            response = client.get("/api/v1/wallets", headers=headers)
            assert response.status_code == 401
    
    def test_expired_token_error(self, authenticated_client: TestClient):
        """Test error with expired token (simulated)."""
        # This would require mocking JWT expiration
        # For now, just test that invalid tokens are rejected
        headers = {"Authorization": "Bearer expired_token_12345"}
        response = authenticated_client.get("/api/v1/wallets", headers=headers)
        assert response.status_code == 401

@pytest.mark.unit
class TestRateLimitingErrors:
    """Test rate limiting error handling (if implemented)."""
    
    def test_potential_rate_limiting(self, authenticated_client: TestClient):
        """Test potential rate limiting on sensitive endpoints."""
        # Make multiple rapid requests to login endpoint
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        # Send multiple failed login attempts
        for _ in range(10):
            response = authenticated_client.post("/api/v1/users/login", json=login_data)
            # Should either return 401 (wrong password) or 429 (rate limited)
            assert response.status_code in [401, 429]

@pytest.mark.unit
class TestErrorResponseFormat:
    """Test error response format consistency."""
    
    def test_error_response_structure(self, client: TestClient):
        """Test that all errors follow consistent response format."""
        # Test different error types
        errors = [
            # 401 Unauthorized
            client.get("/api/v1/wallets"),
            # 404 Not Found  
            client.get("/api/v1/wallets/99999"),
            # 422 Validation Error
            client.post("/api/v1/wallets", json={}),
        ]
        
        for response in errors:
            if response.status_code != 200:  # Error responses
                json_response = response.json()
                assert "detail" in json_response
                assert isinstance(json_response["detail"], str)
                assert len(json_response["detail"]) > 0
    
    def test_validation_error_details(self, client: TestClient):
        """Test validation error provides useful details."""
        response = client.post("/api/v1/users/register", json={
            "email": "invalid-email",
            "password": "123",  # Too short
            "full_name": ""
        })
        
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        
        # Should contain information about what's wrong
        assert isinstance(error_detail, list) or isinstance(error_detail, str)
        
        if isinstance(error_detail, list):
            # FastAPI validation errors are typically arrays
            for error in error_detail:
                assert "loc" in error  # Field location
                assert "msg" in error  # Error message
                assert "type" in error  # Error type

@pytest.mark.unit
class TestEdgeCaseErrors:
    """Test edge case error handling."""
    
    def test_extremely_large_values(self, authenticated_client: TestClient):
        """Test handling of extremely large values."""
        # Very large amount
        response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = response.json()["id"]
        
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 999999999999.99,
            "description": "Very large amount"
        })
        
        # Should either succeed or fail gracefully with proper error
        assert response.status_code in [200, 400, 422]
    
    def test_unicode_and_special_characters(self, authenticated_client: TestClient):
        """Test handling of unicode and special characters."""
        # Unicode in description
        response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = response.json()["id"]
        
        unicode_text = "Payment with émojis 🎉 and ñiño"
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 50.0,
            "description": unicode_text
        })
        
        # Should handle unicode properly
        assert response.status_code == 200
        assert response.json()["description"] == unicode_text
    
    def test_sql_injection_attempts(self, authenticated_client: TestClient):
        """Test that SQL injection attempts are handled safely."""
        # Try SQL injection in description
        response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = response.json()["id"]
        
        sql_injection = "'; DROP TABLE users; --"
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 50.0,
            "description": sql_injection
        })
        
        # Should either succeed (safely stored) or be rejected
        # But should never cause server crash
        assert response.status_code in [200, 400, 422]
        
        # Verify server is still responsive
        health_response = authenticated_client.get("/api/v1/health")
        assert health_response.status_code == 200
