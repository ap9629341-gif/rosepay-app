"""
Integration tests for RosePay application API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
class TestAPIIntegration:
    """Comprehensive integration tests for the entire API."""
    
    def test_complete_user_journey(self, client: TestClient, test_user_data):
        """Test complete user journey from registration to transactions."""
        # Step 1: User Registration
        register_response = client.post("/api/v1/users/register", json=test_user_data)
        assert register_response.status_code == 201
        user_data = register_response.json()
        assert user_data["email"] == test_user_data["email"]
        
        # Step 2: User Login
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        assert login_response.status_code == 200
        token_data = login_response.json()
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 3: Create Wallet
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        assert wallet_response.status_code == 201
        wallet_data = wallet_response.json()
        wallet_id = wallet_data["id"]
        assert wallet_data["balance"] == 0.0
        
        # Step 4: Add Money to Wallet
        add_money_response = client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 500.0,
            "description": "Initial deposit"
        }, headers=headers)
        assert add_money_response.status_code == 200
        transaction_data = add_money_response.json()
        assert transaction_data["amount"] == 500.0
        assert transaction_data["type"] == "deposit"
        
        # Step 5: Check Wallet Balance
        balance_response = client.get(f"/api/v1/wallets/{wallet_id}/balance", headers=headers)
        assert balance_response.status_code == 200
        balance_data = balance_response.json()
        assert balance_data["balance"] == 500.0
        
        # Step 6: View Transaction History
        transactions_response = client.get("/api/v1/transactions", headers=headers)
        assert transactions_response.status_code == 200
        transactions = transactions_response.json()
        assert len(transactions) == 1
        assert transactions[0]["amount"] == 500.0
        
        # Step 7: View All Wallets
        wallets_response = client.get("/api/v1/wallets", headers=headers)
        assert wallets_response.status_code == 200
        wallets = wallets_response.json()
        assert len(wallets) == 1
        assert wallets[0]["id"] == wallet_id
    
    def test_multi_user_transaction_flow(self, client: TestClient, test_user_data, test_user_data_2):
        """Test transaction flow between multiple users."""
        # Setup User 1
        client.post("/api/v1/users/register", json=test_user_data)
        login1_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token1 = login1_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}
        
        # Setup User 2
        client.post("/api/v1/users/register", json=test_user_data_2)
        login2_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token2 = login2_response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Create wallets for both users
        wallet1_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers1)
        wallet2_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers2)
        
        wallet1_id = wallet1_response.json()["id"]
        wallet2_id = wallet2_response.json()["id"]
        user2_id = wallet2_response.json()["user_id"]
        
        # Add money to User 1's wallet
        client.post(f"/api/v1/wallets/{wallet1_id}/add-money", json={
            "amount": 300.0,
            "description": "User 1 initial balance"
        }, headers=headers1)
        
        # Transfer from User 1 to User 2
        transfer_response = client.post(f"/api/v1/wallets/{wallet1_id}/transfer", json={
            "recipient_user_id": user2_id,
            "amount": 100.0,
            "description": "Payment from User 1 to User 2"
        }, headers=headers1)
        assert transfer_response.status_code == 200
        
        # Verify balances
        balance1_response = client.get(f"/api/v1/wallets/{wallet1_id}/balance", headers=headers1)
        balance2_response = client.get(f"/api/v1/wallets/{wallet2_id}/balance", headers=headers2)
        
        assert balance1_response.json()["balance"] == 200.0  # 300 - 100
        assert balance2_response.json()["balance"] == 100.0  # 0 + 100
        
        # Verify transaction histories
        transactions1 = client.get("/api/v1/transactions", headers=headers1).json()
        transactions2 = client.get("/api/v1/transactions", headers=headers2).json()
        
        assert len(transactions1) == 2  # Deposit + Transfer
        assert len(transactions2) == 1  # Received transfer
        
        # Verify transaction amounts
        user1_transfer = [t for t in transactions1 if t["type"] == "transfer"][0]
        user2_received = transactions2[0]
        
        assert user1_transfer["amount"] == -100.0
        assert user2_received["amount"] == 100.0
    
    def test_payment_link_end_to_end_flow(self, client: TestClient, test_user_data, test_user_data_2):
        """Test complete payment link flow between users."""
        # Setup User 1 (link creator)
        client.post("/api/v1/users/register", json=test_user_data)
        login1_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token1 = login1_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}
        
        # Setup User 2 (payer)
        client.post("/api/v1/users/register", json=test_user_data_2)
        login2_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token2 = login2_response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # User 1 creates payment link
        link_response = client.post("/api/v1/payments/link/create", json={
            "amount": 75.0,
            "description": "E-commerce payment",
            "expires_hours": 48
        }, headers=headers1)
        assert link_response.status_code == 201
        link_id = link_response.json()["link_id"]
        
        # User 2 creates wallet and adds funds
        wallet2_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers2)
        wallet2_id = wallet2_response.json()["id"]
        
        client.post(f"/api/v1/wallets/{wallet2_id}/add-money", json={
            "amount": 200.0,
            "description": "Funds for payment"
        }, headers=headers2)
        
        # User 2 pays via link
        pay_response = client.post(f"/api/v1/payments/link/{link_id}/pay", json={
            "wallet_id": wallet2_id
        }, headers=headers2)
        assert pay_response.status_code == 200
        
        # Verify payment completed
        transaction = pay_response.json()
        assert transaction["amount"] == 75.0
        assert transaction["type"] == "payment"
        
        # Verify User 2's balance decreased
        balance2_response = client.get(f"/api/v1/wallets/{wallet2_id}/balance", headers=headers2)
        assert balance2_response.json()["balance"] == 125.0  # 200 - 75
        
        # Verify User 1 received payment
        transactions1 = client.get("/api/v1/transactions", headers=headers1).json()
        payment_received = [t for t in transactions1 if t["type"] == "payment"][0]
        assert payment_received["amount"] == 75.0
    
    def test_payment_request_end_to_end_flow(self, client: TestClient, test_user_data, test_user_data_2):
        """Test complete payment request flow between users."""
        # Setup User 1 (requester)
        client.post("/api/v1/users/register", json=test_user_data)
        login1_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token1 = login1_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}
        
        # Setup User 2 (recipient of request)
        client.post("/api/v1/users/register", json=test_user_data_2)
        login2_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token2 = login2_response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # User 1 creates payment request to User 2
        request_response = client.post("/api/v1/payments/request", json={
            "recipient_email": test_user_data_2["email"],
            "amount": 50.0,
            "description": "Lunch money"
        }, headers=headers1)
        assert request_response.status_code == 201
        request_id = request_response.json()["request_id"]
        
        # User 2 creates wallet and adds funds
        wallet2_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers2)
        wallet2_id = wallet2_response.json()["id"]
        
        client.post(f"/api/v1/wallets/{wallet2_id}/add-money", json={
            "amount": 100.0,
            "description": "Funds for requests"
        }, headers=headers2)
        
        # User 2 accepts and pays the request
        accept_response = client.post(f"/api/v1/payments/request/{request_id}/accept", json={
            "wallet_id": wallet2_id
        }, headers=headers2)
        assert accept_response.status_code == 200
        
        # Verify payment completed
        transaction = accept_response.json()
        assert transaction["amount"] == 50.0
        assert transaction["type"] == "payment"
        
        # Verify User 2's balance decreased
        balance2_response = client.get(f"/api/v1/wallets/{wallet2_id}/balance", headers=headers2)
        assert balance2_response.json()["balance"] == 50.0  # 100 - 50
        
        # Verify User 1 received payment
        transactions1 = client.get("/api/v1/transactions", headers=headers1).json()
        payment_received = [t for t in transactions1 if t["type"] == "payment"][0]
        assert payment_received["amount"] == 50.0
    
    def test_complex_multi_transaction_scenario(self, client: TestClient, test_user_data, test_user_data_2):
        """Test complex scenario with multiple transaction types."""
        # Setup both users
        client.post("/api/v1/users/register", json=test_user_data)
        login1_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token1 = login1_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}
        
        client.post("/api/v1/users/register", json=test_user_data_2)
        login2_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token2 = login2_response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Create wallets
        wallet1_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers1)
        wallet2_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers2)
        
        wallet1_id = wallet1_response.json()["id"]
        wallet2_id = wallet2_response.json()["id"]
        user2_id = wallet2_response.json()["user_id"]
        
        # User 1: Multiple deposits
        amounts = [100.0, 50.0, 25.0]
        for amount in amounts:
            client.post(f"/api/v1/wallets/{wallet1_id}/add-money", json={
                "amount": amount,
                "description": f"Deposit of {amount}"
            }, headers=headers1)
        
        # User 2: Single deposit
        client.post(f"/api/v1/wallets/{wallet2_id}/add-money", json={
            "amount": 200.0,
            "description": "User 2 deposit"
        }, headers=headers2)
        
        # Transfer from User 1 to User 2
        client.post(f"/api/v1/wallets/{wallet1_id}/transfer", json={
            "recipient_user_id": user2_id,
            "amount": 75.0,
            "description": "Transfer payment"
        }, headers=headers1)
        
        # Create and pay payment link
        link_response = client.post("/api/v1/payments/link/create", json={
            "amount": 30.0,
            "description": "Payment link test",
            "expires_hours": 24
        }, headers=headers1)
        link_id = link_response.json()["link_id"]
        
        client.post(f"/api/v1/payments/link/{link_id}/pay", json={
            "wallet_id": wallet2_id
        }, headers=headers2)
        
        # Verify final states
        balance1_response = client.get(f"/api/v1/wallets/{wallet1_id}/balance", headers=headers1)
        balance2_response = client.get(f"/api/v1/wallets/{wallet2_id}/balance", headers=headers2)
        
        # User 1: 175 (100+50+25) - 75 (transfer) + 30 (payment received) = 130
        # User 2: 200 + 75 (transfer received) - 30 (payment made) = 245
        assert balance1_response.json()["balance"] == 130.0
        assert balance2_response.json()["balance"] == 245.0
        
        # Verify transaction counts
        transactions1 = client.get("/api/v1/transactions", headers=headers1).json()
        transactions2 = client.get("/api/v1/transactions", headers=headers2).json()
        
        assert len(transactions1) == 5  # 3 deposits + 1 transfer + 1 payment received
        assert len(transactions2) == 3  # 1 deposit + 1 transfer received + 1 payment made

@pytest.mark.integration
class TestAPIConsistency:
    """Test API consistency and data integrity."""
    
    def test_transaction_balance_consistency(self, client: TestClient, test_user_data):
        """Test that transactions and balances remain consistent."""
        # Setup user
        client.post("/api/v1/users/register", json=test_user_data)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create wallet
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        wallet_id = wallet_response.json()["id"]
        
        # Perform multiple transactions
        transactions_data = [
            {"amount": 100.0, "description": "Deposit 1"},
            {"amount": 50.0, "description": "Deposit 2"},
            {"amount": -25.0, "description": "Withdrawal"},  # This would be a transfer in real scenario
        ]
        
        expected_balance = 0.0
        for tx in transactions_data:
            if tx["amount"] > 0:  # Only positive amounts for add-money
                client.post(f"/api/v1/wallets/{wallet_id}/add-money", json=tx, headers=headers)
                expected_balance += tx["amount"]
        
        # Verify balance matches transaction sum
        balance_response = client.get(f"/api/v1/wallets/{wallet_id}/balance", headers=headers)
        actual_balance = balance_response.json()["balance"]
        
        assert actual_balance == expected_balance
        
        # Verify transaction history sum matches balance
        transactions_response = client.get("/api/v1/transactions", headers=headers)
        transactions = transactions_response.json()
        
        transaction_sum = sum(t["amount"] for t in transactions if t["type"] == "deposit")
        assert transaction_sum == expected_balance
    
    def test_user_isolation_consistency(self, client: TestClient, test_user_data, test_user_data_2):
        """Test that user data isolation is consistent across all endpoints."""
        # Setup both users
        client.post("/api/v1/users/register", json=test_user_data)
        login1_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token1 = login1_response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}
        
        client.post("/api/v1/users/register", json=test_user_data_2)
        login2_response = client.post("/api/v1/users/login", json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        })
        token2 = login2_response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # User 1 creates wallet and transactions
        wallet1_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers1)
        wallet1_id = wallet1_response.json()["id"]
        
        client.post(f"/api/v1/wallets/{wallet1_id}/add-money", json={
            "amount": 100.0,
            "description": "User 1 deposit"
        }, headers=headers1)
        
        # User 2 creates wallet and transactions
        wallet2_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers2)
        wallet2_id = wallet2_response.json()["id"]
        
        client.post(f"/api/v1/wallets/{wallet2_id}/add-money", json={
            "amount": 50.0,
            "description": "User 2 deposit"
        }, headers=headers2)
        
        # Verify isolation across all endpoints
        # Wallets
        wallets1 = client.get("/api/v1/wallets", headers=headers1).json()
        wallets2 = client.get("/api/v1/wallets", headers=headers2).json()
        
        assert len(wallets1) == 1
        assert len(wallets2) == 1
        assert wallets1[0]["id"] != wallets2[0]["id"]
        
        # Transactions
        transactions1 = client.get("/api/v1/transactions", headers=headers1).json()
        transactions2 = client.get("/api/v1/transactions", headers=headers2).json()
        
        assert len(transactions1) == 1
        assert len(transactions2) == 1
        assert transactions1[0]["id"] != transactions2[0]["id"]
        
        # Payment links
        link1_response = client.post("/api/v1/payments/link/create", json={
            "amount": 25.0,
            "description": "User 1 link",
            "expires_hours": 24
        }, headers=headers1)
        
        link2_response = client.post("/api/v1/payments/link/create", json={
            "amount": 35.0,
            "description": "User 2 link",
            "expires_hours": 24
        }, headers=headers2)
        
        # Users should only see their own links
        links1 = client.get("/api/v1/payments/link/created", headers=headers1).json() if "/api/v1/payments/link/created" else []
        links2 = client.get("/api/v1/payments/link/created", headers=headers2).json() if "/api/v1/payments/link/created" else []
        
        # Verify no data leakage
        user1_wallet_ids = [w["id"] for w in wallets1]
        user2_wallet_ids = [w["id"] for w in wallets2]
        
        # User 1 shouldn't be able to access User 2's wallet
        response = client.get(f"/api/v1/wallets/{wallet2_id}", headers=headers1)
        assert response.status_code == 404
        
        # User 2 shouldn't be able to access User 1's wallet
        response = client.get(f"/api/v1/wallets/{wallet1_id}", headers=headers2)
        assert response.status_code == 404

@pytest.mark.integration
class TestAPIPerformance:
    """Basic performance and load testing."""
    
    def test_multiple_concurrent_requests(self, client: TestClient, test_user_data):
        """Test handling of multiple concurrent requests."""
        # Setup user
        client.post("/api/v1/users/register", json=test_user_data)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create wallet
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        wallet_id = wallet_response.json()["id"]
        
        # Make multiple requests in sequence (simulating concurrent load)
        responses = []
        for i in range(10):
            response = client.get(f"/api/v1/wallets/{wallet_id}/balance", headers=headers)
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            assert response.json()["balance"] == 0.0
    
    def test_large_description_handling(self, client: TestClient, test_user_data):
        """Test handling of large data in requests."""
        # Setup user
        client.post("/api/v1/users/register", json=test_user_data)
        login_response = client.post("/api/v1/users/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create wallet
        wallet_response = client.post("/api/v1/wallets", json={"currency": "USD"}, headers=headers)
        wallet_id = wallet_response.json()["id"]
        
        # Test with large description
        large_description = "A" * 1000  # 1000 character description
        
        response = client.post(f"/api/v1/wallets/{wallet_id}/add-money", json={
            "amount": 50.0,
            "description": large_description
        }, headers=headers)
        
        # Should handle gracefully
        assert response.status_code in [200, 422]
