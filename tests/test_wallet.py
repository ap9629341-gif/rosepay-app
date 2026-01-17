"""
Wallet management tests for RosePay application.
"""
import pytest
from fastapi.testclient import TestClient

@pytest.mark.wallet
@pytest.mark.unit
class TestWalletCreation:
    """Test wallet creation functionality."""
    
    def test_create_wallet_success(self, authenticated_client: TestClient, test_wallet_data):
        """Test successful wallet creation."""
        response = authenticated_client.post("/api/v1/wallets", json=test_wallet_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["currency"] == test_wallet_data["currency"]
        assert data["balance"] == 0.0
        assert "id" in data
        assert "created_at" in data
        assert "user_id" in data
    
    def test_create_wallet_multiple_currencies(self, authenticated_client: TestClient):
        """Test creating wallets with different currencies."""
        currencies = ["USD", "EUR", "GBP", "INR"]
        
        for currency in currencies:
            response = authenticated_client.post("/api/v1/wallets", json={"currency": currency})
            assert response.status_code == 200
            assert response.json()["currency"] == currency
    
    def test_create_wallet_invalid_currency_fails(self, authenticated_client: TestClient):
        """Test creating wallet with invalid currency fails."""
        invalid_data = {"currency": "INVALID"}
        
        response = authenticated_client.post("/api/v1/wallets", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_wallet_unauthenticated_fails(self, client: TestClient, test_wallet_data):
        """Test creating wallet without authentication fails."""
        response = client.post("/api/v1/wallets", json=test_wallet_data)
        assert response.status_code == 401
    
    def test_create_wallet_missing_currency_fails(self, authenticated_client: TestClient):
        """Test creating wallet without currency fails."""
        response = authenticated_client.post("/api/v1/wallets", json={})
        assert response.status_code == 422

@pytest.mark.wallet
@pytest.mark.unit
class TestWalletRetrieval:
    """Test wallet retrieval functionality."""
    
    def test_get_user_wallets_empty(self, authenticated_client: TestClient):
        """Test getting wallets when user has none."""
        response = authenticated_client.get("/api/v1/wallets")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_user_wallets_with_data(self, authenticated_client: TestClient):
        """Test getting wallets when user has some."""
        # Create multiple wallets
        wallet1 = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"}).json()
        wallet2 = authenticated_client.post("/api/v1/wallets", json={"currency": "EUR"}).json()
        
        response = authenticated_client.get("/api/v1/wallets")
        
        assert response.status_code == 200
        wallets = response.json()
        assert len(wallets) == 2
        
        wallet_ids = [w["id"] for w in wallets]
        assert wallet1["id"] in wallet_ids
        assert wallet2["id"] in wallet_ids
    
    def test_get_specific_wallet_success(self, authenticated_client: TestClient):
        """Test getting a specific wallet by ID."""
        # Create wallet
        create_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = create_response.json()["id"]
        
        # Get specific wallet
        response = authenticated_client.get(f"/api/v1/wallets/{wallet_id}")
        
        assert response.status_code == 200
        wallet = response.json()
        assert wallet["id"] == wallet_id
        assert wallet["currency"] == "USD"
        assert wallet["balance"] == 0.0
    
    def test_get_specific_wallet_not_found(self, authenticated_client: TestClient):
        """Test getting non-existent wallet fails."""
        response = authenticated_client.get("/api/v1/wallets/99999")
        assert response.status_code == 404
    
    def test_get_other_user_wallet_fails(self, authenticated_client: TestClient, client: TestClient, test_user_data_2):
        """Test accessing another user's wallet fails."""
        # Create wallet for authenticated user
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Create and authenticate second user
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to access first user's wallet
        response = client.get(f"/api/v1/wallets/{wallet_id}", headers=headers)
        assert response.status_code == 404  # Should return 404, not 403 (security)

@pytest.mark.wallet
@pytest.mark.unit
class TestWalletBalance:
    """Test wallet balance functionality."""
    
    def test_get_wallet_balance_initial(self, authenticated_client: TestClient):
        """Test getting initial wallet balance."""
        # Create wallet
        create_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = create_response.json()["id"]
        
        # Get balance
        response = authenticated_client.get(f"/api/v1/wallets/{wallet_id}/balance")
        
        assert response.status_code == 200
        balance_data = response.json()
        assert balance_data["balance"] == 0.0
        assert balance_data["currency"] == "USD"
    
    def test_get_wallet_balance_after_transactions(self, authenticated_client: TestClient):
        """Test getting wallet balance after adding money."""
        # Create wallet
        create_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = create_response.json()["id"]
        
        # Add money
        authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 100.0,
            "description": "Initial deposit"
        })
        
        # Get balance
        response = authenticated_client.get(f"/api/v1/wallets/{wallet_id}/balance")
        
        assert response.status_code == 200
        balance_data = response.json()
        assert balance_data["balance"] == 100.0
        assert balance_data["currency"] == "USD"
    
    def test_get_balance_nonexistent_wallet_fails(self, authenticated_client: TestClient):
        """Test getting balance for non-existent wallet fails."""
        response = authenticated_client.get("/api/v1/wallets/99999/balance")
        assert response.status_code == 404

@pytest.mark.wallet
@pytest.mark.unit
class TestWalletOperations:
    """Test wallet operations like adding money."""
    
    def test_add_money_success(self, authenticated_client: TestClient, test_transaction_data):
        """Test successfully adding money to wallet."""
        # Create wallet
        create_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = create_response.json()["id"]
        
        # Add money
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json=test_transaction_data)
        
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["amount"] == test_transaction_data["amount"]
        assert transaction["description"] == test_transaction_data["description"]
        assert transaction["type"] == "deposit"
        assert transaction["status"] == "completed"
    
    def test_add_money_negative_amount_fails(self, authenticated_client: TestClient):
        """Test adding negative amount fails."""
        # Create wallet
        create_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = create_response.json()["id"]
        
        # Try to add negative amount
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": -50.0,
            "description": "Invalid deposit"
        })
        
        assert response.status_code == 422
    
    def test_add_money_zero_amount_fails(self, authenticated_client: TestClient):
        """Test adding zero amount fails."""
        # Create wallet
        create_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = create_response.json()["id"]
        
        # Try to add zero amount
        response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 0.0,
            "description": "Zero deposit"
        })
        
        assert response.status_code == 422
    
    def test_add_money_unauthenticated_fails(self, client: TestClient, test_transaction_data):
        """Test adding money without authentication fails."""
        response = client.post("/api/v1/wallets/1/add-money", json=test_transaction_data)
        assert response.status_code == 401
    
    def test_add_money_to_other_user_wallet_fails(self, authenticated_client: TestClient, client: TestClient, test_user_data_2, test_transaction_data):
        """Test adding money to another user's wallet fails."""
        # Create wallet for authenticated user
        wallet_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet_id = wallet_response.json()["id"]
        
        # Create and authenticate second user
        client.post("/api/v1/users/register", json=test_user_data_2)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to add money to first user's wallet
        response = client.post(f"/api/v1/wallets/{wallet_id}/add-money", json=test_transaction_data, headers=headers)
        assert response.status_code == 404

@pytest.mark.wallet
@pytest.mark.integration
class TestWalletIntegration:
    """Integration tests for wallet functionality."""
    
    def test_complete_wallet_flow(self, authenticated_client: TestClient):
        """Test complete wallet flow: create -> add money -> check balance -> view transactions."""
        # Step 1: Create wallet
        create_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        assert create_response.status_code == 201
        wallet_id = create_response.json()["id"]
        
        # Step 2: Add money
        add_response = authenticated_client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 150.0,
            "description": "Initial deposit"
        })
        assert add_response.status_code == 200
        
        # Step 3: Check balance
        balance_response = authenticated_client.get(f"/api/v1/wallets/{wallet_id}/balance")
        assert balance_response.status_code == 200
        assert balance_response.json()["balance"] == 150.0
        
        # Step 4: View wallet details
        wallet_response = authenticated_client.get(f"/api/v1/wallets/{wallet_id}")
        assert wallet_response.status_code == 200
        assert wallet_response.json()["balance"] == 150.0
        
        # Step 5: Check transactions
        transactions_response = authenticated_client.get("/api/v1/transactions")
        assert transactions_response.status_code == 200
        transactions = transactions_response.json()
        assert len(transactions) == 1
        assert transactions[0]["amount"] == 150.0
    
    def test_multiple_wallets_isolation(self, authenticated_client: TestClient):
        """Test that operations on one wallet don't affect others."""
        # Create two wallets
        wallet1_response = authenticated_client.post("/api/v1/wallets", json={"currency": "USD"})
        wallet2_response = authenticated_client.post("/api/v1/wallets", json={"currency": "EUR"})
        
        wallet1_id = wallet1_response.json()["id"]
        wallet2_id = wallet2_response.json()["id"]
        
        # Add money to first wallet only
        authenticated_client.post(f"/api/v1/wallets/{wallet1_id}/add-money", json={
            "amount": 100.0,
            "description": "USD deposit"
        })
        
        # Check balances
        balance1_response = authenticated_client.get(f"/api/v1/wallets/{wallet1_id}/balance")
        balance2_response = authenticated_client.get(f"/api/v1/wallets/{wallet2_id}/balance")
        
        assert balance1_response.json()["balance"] == 100.0
        assert balance2_response.json()["balance"] == 0.0
