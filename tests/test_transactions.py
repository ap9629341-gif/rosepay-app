"""
Transaction tests for RosePay application.
"""
import pytest
from fastapi.testclient import TestClient

@pytest.mark.transaction
@pytest.mark.unit
class TestTransactionHistory:
    """Test transaction history functionality."""
    
    def test_get_transactions_empty(self, authenticated_client: TestClient):
        """Test getting transactions when user has none."""
        response = authenticated_client.get("/api/v1/transactions")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_transactions_with_data(self, authenticated_client: TestClient):
        """Test getting transactions when user has some."""
        # Create wallet and add money
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Add money multiple times
        authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0,
            "description": "First deposit"
        })
        authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 50.0,
            "description": "Second deposit"
        })
        
        # Get transactions
        response = authenticated_client.get("/api/v1/transactions")
        
        assert response.status_code == 200
        transactions = response.json()
        assert len(transactions) == 2
        
        # Verify transaction details
        amounts = [t["amount"] for t in transactions]
        assert 100.0 in amounts
        assert 50.0 in amounts
    
    def test_get_specific_transaction_success(self, authenticated_client: TestClient):
        """Test getting a specific transaction by ID."""
        # Create wallet and add money
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        add_response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0,
            "description": "Test deposit"
        })
        transaction_id = add_response.json()["id"]
        
        # Get specific transaction
        response = authenticated_client.get(f"/api/v1/transactions/{transaction_id}")
        
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["id"] == transaction_id
        assert transaction["amount"] == 100.0
        assert transaction["description"] == "Test deposit"
        assert transaction["type"] == "deposit"
    
    def test_get_specific_transaction_not_found(self, authenticated_client: TestClient):
        """Test getting non-existent transaction fails."""
        response = authenticated_client.get("/api/v1/transactions/99999")
        assert response.status_code == 404
    
    def test_get_other_user_transaction_fails(self, authenticated_client: TestClient, client: TestClient, test_user_data_2):
        """Test accessing another user's transaction fails."""
        # Create wallet and transaction for authenticated user
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        add_response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0,
            "description": "Test deposit"
        })
        transaction_id = add_response.json()["id"]
        
        # Create and authenticate second user
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to access first user's transaction
        response = client.get(f"/api/v1/transactions/{transaction_id}", headers=headers)
        assert response.status_code == 404

@pytest.mark.transaction
@pytest.mark.unit
class TestMoneyTransfer:
    """Test money transfer functionality."""
    
    def test_transfer_money_success(self, authenticated_client: TestClient, client: TestClient, test_user_data_2):
        """Test successful money transfer between users."""
        # Setup sender wallet
        sender_wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        sender_wallet_id = sender_wallet_response.json()["id"]
        
        # Add money to sender wallet
        authenticated_client.post(f"/api/v1/wallets/{sender_wallet_id}/add-money", json={
            "amount": 200.0,
            "description": "Initial balance"
        })
        
        # Setup recipient
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        recipient_wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        recipient_wallet_id = recipient_wallet_response.json()["id"]
        
        # Get recipient user ID from wallet details
        recipient_wallet_details = client.get(f"/api/v1/wallets/{recipient_wallet_id}", headers=headers)
        recipient_user_id = recipient_wallet_details.json()["user_id"]
        
        # Perform transfer
        transfer_response = authenticated_client.post(f"/api/v1/wallets/{sender_wallet_id}/transfer", json={
            "recipient_user_id": recipient_user_id,
            "amount": 50.0,
            "description": "Payment for services"
        })
        
        assert transfer_response.status_code == 200
        transaction = transfer_response.json()
        assert transaction["amount"] == 50.0
        assert transaction["type"] == "transfer"
        assert transaction["status"] == "completed"
    
    def test_transfer_insufficient_funds_fails(self, authenticated_client: TestClient):
        """Test transfer with insufficient funds fails."""
        # Create wallet with small balance
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 10.0,
            "description": "Small balance"
        })
        
        # Try to transfer more than available
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/transfer", json={
            "recipient_user_id": 999,  # Non-existent user ID
            "amount": 50.0,
            "description": "Too much transfer"
        })
        
        assert response.status_code == 400
        assert "insufficient" in response.json()["detail"].lower()
    
    def test_transfer_negative_amount_fails(self, authenticated_client: TestClient):
        """Test transfer with negative amount fails."""
        # Create wallet
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Try to transfer negative amount
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/transfer", json={
            "recipient_user_id": 999,
            "amount": -25.0,
            "description": "Negative transfer"
        })
        
        assert response.status_code == 422
    
    def test_transfer_zero_amount_fails(self, authenticated_client: TestClient):
        """Test transfer with zero amount fails."""
        # Create wallet
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Try to transfer zero amount
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/transfer", json={
            "recipient_user_id": 999,
            "amount": 0.0,
            "description": "Zero transfer"
        })
        
        assert response.status_code == 422
    
    def test_transfer_to_self_fails(self, authenticated_client: TestClient):
        """Test transfer to self fails."""
        # Create wallet
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Get user ID from wallet
        user_id = wallet_response.json()["user_id"]
        
        # Try to transfer to self
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/transfer", json={
            "recipient_user_id": user_id,
            "amount": 25.0,
            "description": "Self transfer"
        })
        
        assert response.status_code == 400
        assert "yourself" in response.json()["detail"].lower()
    
    def test_transfer_unauthenticated_fails(self, client: TestClient):
        """Test transfer without authentication fails."""
        response = client.post("/api/v1/wallets/1/transfer", json={
            "recipient_user_id": 999,
            "amount": 25.0,
            "description": "Unauthenticated transfer"
        })
        
        assert response.status_code == 401

@pytest.mark.transaction
@pytest.mark.unit
class TestTransactionValidation:
    """Test transaction validation and edge cases."""
    
    def test_transaction_amount_precision(self, authenticated_client: TestClient):
        """Test transaction amount with decimal precision."""
        # Create wallet
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Add money with decimal places
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 123.456,
            "description": "Decimal amount test"
        })
        
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["amount"] == 123.456
    
    def test_transaction_description_length(self, authenticated_client: TestClient):
        """Test transaction with long description."""
        # Create wallet
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Add money with long description
        long_description = "A" * 500  # Very long description
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0,
            "description": long_description
        })
        
        # Should either succeed or fail gracefully based on validation
        assert response.status_code in [200, 422]
    
    def test_transaction_missing_description(self, authenticated_client: TestClient):
        """Test transaction without description."""
        # Create wallet
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Try to add money without description
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0
        })
        
        assert response.status_code == 422

@pytest.mark.transaction
@pytest.mark.integration
class TestTransactionIntegration:
    """Integration tests for transaction functionality."""
    
    def test_complete_transfer_flow(self, authenticated_client: TestClient, client: TestClient, test_user_data_2):
        """Test complete transfer flow with balance updates."""
        # Setup sender
        sender_wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        sender_wallet_id = sender_wallet_response.json()["id"]
        
        authenticated_client.post(f"/api/v1/wallets/{sender_wallet_id}/add-money", json={
            "amount": 200.0,
            "description": "Initial balance"
        })
        
        # Setup recipient
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        recipient_wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        recipient_wallet_id = recipient_wallet_response.json()["id"]
        
        recipient_wallet_details = client.get(f"/api/v1/wallets/{recipient_wallet_id}", headers=headers)
        recipient_user_id = recipient_wallet_details.json()["user_id"]
        
        # Check initial balances
        sender_balance_before = authenticated_client.get(f"/api/v1/wallets/{sender_wallet_id}/balance")
        recipient_balance_before = client.get(f"/api/v1/wallets/{recipient_wallet_id}/balance", headers=headers)
        
        assert sender_balance_before.json()["balance"] == 200.0
        assert recipient_balance_before.json()["balance"] == 0.0
        
        # Perform transfer
        transfer_response = authenticated_client.post(f"/api/v1/wallets/{sender_wallet_id}/transfer", json={
            "recipient_user_id": recipient_user_id,
            "amount": 75.0,
            "description": "Complete flow test"
        })
        
        assert transfer_response.status_code == 200
        
        # Check final balances
        sender_balance_after = authenticated_client.get(f"/api/v1/wallets/{sender_wallet_id}/balance")
        recipient_balance_after = client.get(f"/api/v1/wallets/{recipient_wallet_id}/balance", headers=headers)
        
        assert sender_balance_after.json()["balance"] == 125.0  # 200 - 75
        assert recipient_balance_after.json()["balance"] == 75.0   # 0 + 75
        
        # Check transaction histories
        sender_transactions = authenticated_client.get("/api/v1/transactions")
        recipient_transactions = client.get("/api/v1/transactions", headers=headers)
        
        assert len(sender_transactions.json()) == 2  # Initial deposit + transfer
        assert len(recipient_transactions.json()) == 1  # Received transfer
        
        # Verify transaction details
        sender_transfer = [t for t in sender_transactions.json() if t["type"] == "transfer"][0]
        recipient_transfer = recipient_transactions.json()[0]
        
        assert sender_transfer["amount"] == -75.0  # Money sent
        assert recipient_transfer["amount"] == 75.0  # Money received
    
    def test_transaction_ordering(self, authenticated_client: TestClient):
        """Test that transactions are returned in chronological order."""
        # Create wallet
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Add multiple transactions
        transactions = []
        for i in range(5):
            response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
                "amount": float(i + 1) * 10.0,
                "description": f"Transaction {i + 1}"
            })
            transactions.append(response.json())
        
        # Get all transactions
        response = authenticated_client.get("/api/v1/transactions")
        all_transactions = response.json()
        
        assert len(all_transactions) == 5
        
        # Check that they're ordered by creation time (newest first typically)
        timestamps = [t["created_at"] for t in all_transactions]
        assert timestamps == sorted(timestamps, reverse=True)  # Assuming newest first
