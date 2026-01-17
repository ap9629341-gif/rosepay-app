#!/bin/bash

# RosePay Test Runner Script
# This script runs the comprehensive test suite for the RosePay payment application

echo "🌹 RosePay Test Suite Runner"
echo "================================"

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "💡 It's recommended to run tests in a virtual environment"
    echo ""
fi

# Install test dependencies if needed
echo "📦 Installing test dependencies..."
python3 -m pip install -r requirements.txt

# Run different test suites
echo ""
echo "🧪 Running Authentication Tests..."
python3 -m pytest tests/test_auth.py -v --tb=short

echo ""
echo "💰 Running Wallet Tests..."
python3 -m pytest tests/test_wallet.py -v --tb=short

echo ""
echo "🔄 Running Transaction Tests..."
python3 -m pytest tests/test_transactions.py -v --tb=short

echo ""
echo "💳 Running Payment Tests..."
python3 -m pytest tests/test_payments.py -v --tb=short

echo ""
echo "❌ Running Error Handling Tests..."
python3 -m pytest tests/test_errors.py -v --tb=short

echo ""
echo "🔗 Running Integration Tests..."
python3 -m pytest tests/test_integration.py -v --tb=short

echo ""
echo "📊 Running Full Test Suite with Coverage..."
python3 -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=80

echo ""
echo "✅ Test Suite Complete!"
echo "📈 Coverage report generated in htmlcov/"
echo "🌐 Open htmlcov/index.html to view detailed coverage report"

# Run specific test categories if requested
if [[ "$1" == "unit" ]]; then
    echo ""
    echo "🔬 Running Unit Tests Only..."
    python3 -m pytest tests/ -v -m "unit" --tb=short
elif [[ "$1" == "integration" ]]; then
    echo ""
    echo "🔗 Running Integration Tests Only..."
    python3 -m pytest tests/ -v -m "integration" --tb=short
elif [[ "$1" == "auth" ]]; then
    echo ""
    echo "🔐 Running Authentication Tests Only..."
    python3 -m pytest tests/ -v -m "auth" --tb=short
fi

echo ""
echo "🎯 Quick Test Commands:"
echo "  ./run_tests.sh              - Run all tests"
echo "  ./run_tests.sh unit         - Run unit tests only"
echo "  ./run_tests.sh integration  - Run integration tests only"
echo "  ./run_tests.sh auth         - Run authentication tests only"
echo "  python3 -m pytest tests/ -v            - Run with pytest directly"
echo "  python3 -m pytest tests/test_auth.py   - Run specific test file"
