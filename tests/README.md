# RosePay Test Suite

This directory contains the comprehensive test suite for the RosePay payment application.

## Test Structure

### Test Files

- **`test_auth.py`** - Authentication and authorization tests
  - User registration and login
  - JWT token validation
  - Authentication error handling

- **`test_wallet.py`** - Wallet management tests
  - Wallet creation and retrieval
  - Balance operations
  - Wallet security and isolation

- **`test_transactions.py`** - Transaction tests
  - Money transfers between users
  - Transaction history
  - Transfer validation and limits

- **`test_payments.py`** - Payment link and request tests
  - Payment link creation and QR codes
  - Payment via links
  - Payment requests and acceptance

- **`test_errors.py`** - Error handling and validation tests
  - Input validation
  - Business logic errors
  - Edge cases and security

- **`test_integration.py`** - Integration tests
  - End-to-end user journeys
  - Multi-user scenarios
  - API consistency tests

### Configuration Files

- **`conftest.py`** - Pytest configuration and fixtures
- **`pytest.ini`** - Pytest settings and coverage configuration

## Running Tests

### Quick Start

```bash
# Run all tests
./run_tests.sh

# Run with pytest directly
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Categories

```bash
# Run unit tests only
pytest tests/ -m "unit"

# Run integration tests only
pytest tests/ -m "integration"

# Run authentication tests only
pytest tests/ -m "auth"

# Run wallet tests only
pytest tests/ -m "wallet"

# Run transaction tests only
pytest tests/ -m "transaction"

# Run payment tests only
pytest tests/ -m "payment"
```

### Individual Test Files

```bash
# Run authentication tests
pytest tests/test_auth.py -v

# Run wallet tests
pytest tests/test_wallet.py -v

# Run transaction tests
pytest tests/test_transactions.py -v

# Run payment tests
pytest tests/test_payments.py -v

# Run error handling tests
pytest tests/test_errors.py -v

# Run integration tests
pytest tests/test_integration.py -v
```

## Test Coverage

The test suite aims for **80%+ code coverage** across:

- ✅ Authentication endpoints
- ✅ Wallet management endpoints
- ✅ Transaction endpoints
- ✅ Payment link and request endpoints
- ✅ Error handling
- ✅ Input validation
- ✅ Security scenarios

## Test Fixtures

### Available Fixtures

- **`client`** - FastAPI test client with test database
- **`db_session`** - Database session for testing
- **`test_user_data`** - Sample user registration data
- **`test_user_data_2`** - Second sample user data
- **`authenticated_client`** - Pre-authenticated test client
- **`test_wallet_data`** - Sample wallet creation data
- **`test_transaction_data`** - Sample transaction data
- **`test_payment_link_data`** - Sample payment link data
- **`test_payment_request_data`** - Sample payment request data

### Test Database

Tests use a separate SQLite database (`test_wallet_app.db`) that is:

- Created before each test session
- Isolated from the development database
- Cleaned up after tests complete
- Populated with fresh data for each test

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual functions and methods
- Fast and focused
- Mock external dependencies when needed

### Integration Tests (`@pytest.mark.integration`)
- Test multiple components working together
- End-to-end user workflows
- Database interactions
- API endpoint integration

### Feature-Specific Tests
- **`@pytest.mark.auth`** - Authentication related tests
- **`@pytest.mark.wallet`** - Wallet related tests
- **`@pytest.mark.transaction`** - Transaction related tests
- **`@pytest.mark.payment`** - Payment related tests

## Test Scenarios Covered

### Authentication
- ✅ User registration with valid/invalid data
- ✅ User login with correct/incorrect credentials
- ✅ JWT token generation and validation
- ✅ Token expiration and refresh
- ✅ Unauthorized access protection

### Wallet Management
- ✅ Wallet creation with different currencies
- ✅ Wallet balance retrieval
- ✅ Adding money to wallets
- ✅ Wallet ownership and security
- ✅ Multiple wallets per user

### Transactions
- ✅ Money transfers between users
- ✅ Transaction history and details
- ✅ Insufficient funds handling
- ✅ Transaction validation and limits
- ✅ Self-transfer prevention

### Payments
- ✅ Payment link creation and sharing
- ✅ QR code generation
- ✅ Payment via links
- ✅ Payment requests and acceptance
- ✅ Payment link expiration

### Error Handling
- ✅ Input validation errors
- ✅ Business logic errors
- ✅ Authentication errors
- ✅ Resource not found errors
- ✅ Edge cases and security

### Integration
- ✅ Complete user journeys
- ✅ Multi-user transactions
- ✅ Payment link end-to-end flow
- ✅ Payment request end-to-end flow
- ✅ Complex transaction scenarios

## Coverage Reports

After running tests with coverage:

```bash
# View coverage in terminal
pytest tests/ --cov=. --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=. --cov-report=html

# View detailed HTML report
open htmlcov/index.html
```

## Best Practices

### Writing New Tests

1. **Use descriptive test names** that explain what is being tested
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Use appropriate fixtures** to avoid code duplication
4. **Test both success and failure scenarios**
5. **Add meaningful assertions** with clear error messages
6. **Use test markers** to categorize tests

### Example Test Structure

```python
@pytest.mark.wallet
@pytest.mark.unit
def test_create_wallet_success(authenticated_client, test_wallet_data):
    """Test successful wallet creation."""
    # Arrange
    # (test data prepared by fixtures)
    
    # Act
    response = authenticated_client.post("/api/v1/wallets", json=test_wallet_data)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["currency"] == test_wallet_data["currency"]
    assert data["balance"] == 0.0
```

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Ensure test database permissions
   - Check SQLite file location

2. **Import errors**
   - Install test dependencies: `pip install -r requirements.txt`
   - Check Python path configuration

3. **Authentication failures in tests**
   - Ensure `authenticated_client` fixture is used
   - Check token generation in fixtures

4. **Coverage below threshold**
   - Add tests for uncovered code paths
   - Check coverage report for missing lines

### Debugging Tests

```bash
# Run with verbose output
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x

# Run specific test with debugging
pytest tests/test_auth.py::TestUserLogin::test_login_success -v -s

# Show local variables on failure
pytest tests/ --tb=long
```

## Contributing

When adding new features:

1. **Write tests first** (TDD approach)
2. **Cover all edge cases**
3. **Add integration tests** for complex workflows
4. **Update documentation**
5. **Ensure coverage stays above 80%**

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

- Fast execution for quick feedback
- Coverage reporting for quality gates
- Parallel execution support
- Clear error reporting for debugging
