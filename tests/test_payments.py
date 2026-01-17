"""
Payment link and request tests for RosePay application.
"""
import pytest
from fastapi.testclient import TestClient

@pytest.mark.payment
@pytest.mark.unit
class TestPaymentLinks:
    """Test payment link functionality."""
    
    def test_create_payment_link_success(self, authenticated_client: TestClient, test_payment_link_data):
        """Test successful payment link creation."""
        response = authenticated_client.post("/api/v1/payments/link/create", json=test_payment_link_data)
        
        assert response.status_code == 200
        link_data = response.json()
        assert link_data["amount"] == test_payment_link_data["amount"]
        assert link_data["description"] == test_payment_link_data["description"]
        assert "link_id" in link_data
        assert "expires_at" in link_data
        assert link_data["is_active"] == True
    
    def test_create_payment_link_different_amounts(self, authenticated_client: TestClient):
        """Test creating payment links with different amounts."""
        amounts = [10.0, 25.50, 100.0, 999.99]
        
        for amount in amounts:
            response = authenticated_client.post("/api/v1/payments/link/create", json={
                "amount": amount,
                "description": f"Payment link for {amount}",
                "expires_hours": 24
            })
            
            assert response.status_code == 201
            assert response.json()["amount"] == amount
    
    def test_create_payment_link_invalid_amount_fails(self, authenticated_client: TestClient):
        """Test creating payment link with invalid amount fails."""
        # Negative amount
        response = authenticated_client.post("/api/v1/payments/link/create", json={
            "amount": -50.0,
            "description": "Invalid negative amount",
            "expires_hours": 24
        })
        assert response.status_code == 422
        
        # Zero amount
        response = authenticated_client.post("/api/v1/payments/link/create", json={
            "amount": 0.0,
            "description": "Invalid zero amount",
            "expires_hours": 24
        })
        assert response.status_code == 422
    
    def test_create_payment_link_invalid_expiry_fails(self, authenticated_client: TestClient):
        """Test creating payment link with invalid expiry fails."""
        # Negative expiry
        response = authenticated_client.post("/api/v1/payments/link/create", json={
            "amount": 50.0,
            "description": "Invalid expiry",
            "expires_hours": -24
        })
        assert response.status_code == 422
        
        # Zero expiry
        response = authenticated_client.post("/api/v1/payments/link/create", json={
            "amount": 50.0,
            "description": "Zero expiry",
            "expires_hours": 0
        })
        assert response.status_code == 422
    
    def test_create_payment_link_unauthenticated_fails(self, client: TestClient, test_payment_link_data):
        """Test creating payment link without authentication fails."""
        response = client.post("/api/v1/payments/link/create", json=test_payment_link_data)
        assert response.status_code == 401
    
    def test_get_payment_link_success(self, authenticated_client: TestClient, test_payment_link_data):
        """Test getting payment link details."""
        # Create payment link
        create_response = authenticated_client.post("/api/v1/payments/link/create", json=test_payment_link_data)
        link_id = create_response.json()["link_id"]
        
        # Get payment link
        response = authenticated_client.get(f"/api/v1/payments/link/{link_id}")
        
        assert response.status_code == 200
        link_data = response.json()
        assert link_data["link_id"] == link_id
        assert link_data["amount"] == test_payment_link_data["amount"]
        assert link_data["description"] == test_payment_link_data["description"]
    
    def test_get_payment_link_not_found(self, authenticated_client: TestClient):
        """Test getting non-existent payment link fails."""
        response = authenticated_client.get("/api/v1/payments/link/nonexistent")
        assert response.status_code == 404
    
    def test_get_other_user_payment_link_fails(self, authenticated_client: TestClient, client: TestClient, test_user_data_2):
        """Test accessing another user's payment link fails."""
        # Create payment link for authenticated user
        create_response = authenticated_client.post("/api/v1/payments/link/create", json={
            "amount": 50.0,
            "description": "User 1 link",
            "expires_hours": 24
        })
        link_id = create_response.json()["link_id"]
        
        # Create and authenticate second user
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to access first user's payment link
        response = client.get(f"/api/v1/payments/link/{link_id}", headers=headers)
        assert response.status_code == 404

@pytest.mark.payment
@pytest.mark.unit
class TestPaymentLinkPayment:
    """Test paying via payment links."""
    
    def test_pay_via_link_success(self, authenticated_client: TestClient, client: TestClient, test_user_data_2, test_payment_link_data):
        """Test successful payment via link."""
        # Create payment link for user 1
        create_response = authenticated_client.post("/api/v1/payments/link/create", json=test_payment_link_data)
        link_id = create_response.json()["link_id"]
        
        # Setup user 2 with wallet and balance
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create wallet for user 2 and add money
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        wallet_id = wallet_response.json()["id"]
        
        client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0,
            "description": "Initial balance"
        }, headers=headers)
        
        # Pay via link
        response = client.post(f"/api/v1/payments/link/{link_id}/pay", json={
            "wallet_id": wallet_id
        }, headers=headers)
        
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["amount"] == test_payment_link_data["amount"]
        assert transaction["type"] == "payment"
        assert transaction["status"] == "completed"
    
    def test_pay_via_link_insufficient_funds_fails(self, authenticated_client: TestClient, client: TestClient, test_user_data_2, test_payment_link_data):
        """Test paying via link with insufficient funds fails."""
        # Create payment link for user 1
        create_response = authenticated_client.post("/api/v1/payments/link/create", json=test_payment_link_data)
        link_id = create_response.json()["link_id"]
        
        # Setup user 2 with wallet but no balance
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create wallet for user 2 (no money added)
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        wallet_id = wallet_response.json()["id"]
        
        # Try to pay via link
        response = client.post(f"/api/v1/payments/link/{link_id}/pay", json={
            "wallet_id": wallet_id
        }, headers=headers)
        
        assert response.status_code == 400
        assert "insufficient" in response.json()["detail"].lower()
    
    def test_pay_via_link_invalid_wallet_fails(self, authenticated_client: TestClient, client: TestClient, test_user_data_2, test_payment_link_data):
        """Test paying via link with invalid wallet fails."""
        # Create payment link for user 1
        create_response = authenticated_client.post("/api/v1/payments/link/create", json=test_payment_link_data)
        link_id = create_response.json()["link_id"]
        
        # Setup user 2
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to pay with non-existent wallet
        response = client.post(f"/api/v1/payments/link/{link_id}/pay", json={
            "wallet_id": 99999
        }, headers=headers)
        
        assert response.status_code == 404
    
    def test_pay_via_link_unauthenticated_fails(self, client: TestClient):
        """Test paying via link without authentication fails."""
        response = client.post("/api/v1/payments/link/somelink/pay", json={
            "wallet_id": 1
        })
        assert response.status_code == 401

@pytest.mark.payment
@pytest.mark.unit
class TestPaymentQR:
    """Test QR code generation for payment links."""
    
    def test_get_payment_qr_success(self, authenticated_client: TestClient, test_payment_link_data):
        """Test getting QR code for payment link."""
        # Create payment link
        create_response = authenticated_client.post("/api/v1/payments/link/create", json=test_payment_link_data)
        link_id = create_response.json()["link_id"]
        
        # Get QR code
        response = authenticated_client.get(f"/api/v1/payments/link/{link_id}/qr")
        
        assert response.status_code == 200
        qr_data = response.json()
        assert "qr_code" in qr_data
        assert qr_data["link_id"] == link_id
        assert qr_data["amount"] == test_payment_link_data["amount"]
    
    def test_get_payment_qr_nonexistent_link_fails(self, authenticated_client: TestClient):
        """Test getting QR code for non-existent link fails."""
        response = authenticated_client.get("/api/v1/payments/link/nonexistent/qr")
        assert response.status_code == 404

@pytest.mark.payment
@pytest.mark.unit
class TestPaymentRequests:
    """Test payment request functionality."""
    
    def test_create_payment_request_success(self, authenticated_client: TestClient, test_payment_request_data):
        """Test successful payment request creation."""
        response = authenticated_client.post("/api/v1/payments/request", json=test_payment_request_data)
        
        assert response.status_code == 200
        request_data = response.json()
        assert request_data["recipient_email"] == test_payment_request_data["recipient_email"]
        assert request_data["amount"] == test_payment_request_data["amount"]
        assert request_data["description"] == test_payment_request_data["description"]
        assert "request_id" in request_data
        assert request_data["status"] == "pending"
    
    def test_create_payment_request_invalid_amount_fails(self, authenticated_client: TestClient):
        """Test creating payment request with invalid amount fails."""
        # Negative amount
        response = authenticated_client.post("/api/v1/payments/request", json={
            "recipient_email": "test@example.com",
            "amount": -25.0,
            "description": "Invalid negative request"
        })
        assert response.status_code == 422
    
    def test_create_payment_request_invalid_email_fails(self, authenticated_client: TestClient):
        """Test creating payment request with invalid email fails."""
        response = authenticated_client.post("/api/v1/payments/request", json={
            "recipient_email": "invalid-email",
            "amount": 25.0,
            "description": "Invalid email request"
        })
        assert response.status_code == 422
    
    def test_create_payment_request_unauthenticated_fails(self, client: TestClient, test_payment_request_data):
        """Test creating payment request without authentication fails."""
        response = client.post("/api/v1/payments/request", json=test_payment_request_data)
        assert response.status_code == 401
    
    def test_get_received_payment_requests_empty(self, authenticated_client: TestClient):
        """Test getting received payment requests when none exist."""
        response = authenticated_client.get("/api/v1/payments/request/received")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_sent_payment_requests_empty(self, authenticated_client: TestClient):
        """Test getting sent payment requests when none exist."""
        response = authenticated_client.get("/api/v1/payments/request/sent")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_accept_payment_request_success(self, authenticated_client: TestClient, client: TestClient, test_user_data_2, test_payment_request_data):
        """Test accepting and paying a payment request."""
        # Setup user 1 (requester)
        # Setup user 2 (recipient) - update test_payment_request_data to use test_user_data_2 email
        test_payment_request_data["recipient_email"] = test_user_data_2["email"]
        
        # Create payment request from user 1 to user 2
        create_response = authenticated_client.post("/api/v1/payments/request", json=test_payment_request_data)
        request_id = create_response.json()["request_id"]
        
        # Setup user 2 with wallet and balance
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create wallet for user 2 and add money
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        wallet_id = wallet_response.json()["id"]
        
        client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0,
            "description": "Initial balance"
        }, headers=headers)
        
        # Accept payment request
        response = client.post(f"/api/v1/payments/request/{request_id}/accept", json={
            "wallet_id": wallet_id
        }, headers=headers)
        
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["amount"] == test_payment_request_data["amount"]
        assert transaction["type"] == "payment"
        assert transaction["status"] == "completed"
    
    def test_accept_payment_request_insufficient_funds_fails(self, authenticated_client: TestClient, client: TestClient, test_user_data_2, test_payment_request_data):
        """Test accepting payment request with insufficient funds fails."""
        # Setup user 1 (requester)
        test_payment_request_data["recipient_email"] = test_user_data_2["email"]
        
        # Create payment request from user 1 to user 2
        create_response = authenticated_client.post("/api/v1/payments/request", json=test_payment_request_data)
        request_id = create_response.json()["request_id"]
        
        # Setup user 2 with wallet but no balance
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create wallet for user 2 (no money added)
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        wallet_id = wallet_response.json()["id"]
        
        # Try to accept payment request
        response = client.post(f"/api/v1/payments/request/{request_id}/accept", json={
            "wallet_id": wallet_id
        }, headers=headers)
        
        assert response.status_code == 400
        assert "insufficient" in response.json()["detail"].lower()

@pytest.mark.payment
@pytest.mark.integration
class TestPaymentIntegration:
    """Integration tests for payment functionality."""
    
    def test_complete_payment_link_flow(self, authenticated_client: TestClient, client: TestClient, test_user_data_2):
        """Test complete payment link flow: create -> share -> pay -> verify."""
        # Step 1: Create payment link
        link_response = authenticated_client.post("/api/v1/payments/link/create", json={
            "amount": 75.0,
            "description": "Complete flow test",
            "expires_hours": 24
        })
        assert link_response.status_code == 201
        link_id = link_response.json()["link_id"]
        
        # Step 2: Get QR code
        qr_response = authenticated_client.get(f"/api/v1/payments/link/{link_id}/qr")
        assert qr_response.status_code == 200
        assert "qr_code" in qr_response.json()
        
        # Step 3: Setup payer
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        wallet_id = wallet_response.json()["id"]
        
        client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0,
            "description": "Payment balance"
        }, headers=headers)
        
        # Step 4: Pay via link
        pay_response = client.post(f"/api/v1/payments/link/{link_id}/pay", json={
            "wallet_id": wallet_id
        }, headers=headers)
        assert pay_response.status_code == 200
        
        # Step 5: Verify transaction in both accounts
        payer_transactions = client.get("/api/v1/transactions", headers=headers)
        payee_transactions = authenticated_client.get("/api/v1/transactions")
        
        assert len(payer_transactions.json()) == 1
        assert len(payee_transactions.json()) == 1
        
        payer_transaction = payer_transactions.json()[0]
        payee_transaction = payee_transactions.json()[0]
        
        assert payer_transaction["amount"] == -75.0
        assert payee_transaction["amount"] == 75.0
        assert payer_transaction["type"] == "payment"
        assert payee_transaction["type"] == "payment"
