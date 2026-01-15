"""
Transaction limits and validation service.

WHAT THIS FILE DOES:
- Validates transaction amounts (min/max limits)
- Checks daily transaction limits
- Prevents fraud and excessive transactions

LEARN:
- Transaction limits protect users and prevent fraud
- Daily limits prevent large losses if account is compromised
- Min limits prevent spam transactions
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from config import settings
from models import Transaction, TransactionStatus


def validate_transaction_amount(amount: float) -> None:
    """
    Validate transaction amount against limits.
    
    WHAT IT DOES:
    1. Checks if amount is too small (minimum limit)
    2. Checks if amount is too large (maximum limit)
    3. Raises error if limits exceeded
    
    EXAMPLE:
    - Min: $0.01 (can't send less than 1 cent)
    - Max: $10,000 (can't send more than $10k in one transaction)
    """
    if amount < settings.MIN_TRANSACTION_AMOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Amount too small. Minimum is ${settings.MIN_TRANSACTION_AMOUNT:.2f}"
        )
    
    if amount > settings.MAX_TRANSACTION_AMOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Amount too large. Maximum is ${settings.MAX_TRANSACTION_AMOUNT:.2f}"
        )


def check_daily_transaction_limit(
    db: Session,
    user_id: int,
    wallet_id: int,
    new_transaction_amount: float
) -> None:
    """
    Check if user has exceeded daily transaction limit.
    
    WHAT IT DOES:
    1. Gets all transactions for today
    2. Sums up total amount
    3. Adds new transaction amount
    4. Checks if exceeds daily limit
    5. Raises error if limit exceeded
    
    EXAMPLE:
    - Daily limit: $50,000
    - Today's transactions: $45,000
    - New transaction: $10,000
    - Total: $55,000 → EXCEEDS LIMIT → Error!
    """
    # Get start of today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get all completed transactions for today
    today_transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.wallet_id == wallet_id,
        Transaction.status == TransactionStatus.COMPLETED,
        Transaction.created_at >= today_start
    ).all()
    
    # Calculate total for today
    today_total = sum(t.amount for t in today_transactions)
    
    # Add new transaction amount
    total_with_new = today_total + new_transaction_amount
    
    # Check if exceeds limit
    if total_with_new > settings.DAILY_TRANSACTION_LIMIT:
        remaining = settings.DAILY_TRANSACTION_LIMIT - today_total
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Daily transaction limit exceeded. You can transact ${remaining:.2f} more today. Daily limit: ${settings.DAILY_TRANSACTION_LIMIT:.2f}"
        )


def validate_transaction(
    db: Session,
    user_id: int,
    wallet_id: int,
    amount: float
) -> None:
    """
    Complete validation for a transaction.
    
    WHAT IT DOES:
    1. Validates amount (min/max)
    2. Checks daily limit
    3. Raises errors if validation fails
    
    USAGE:
    Call this before processing any transaction!
    """
    # Validate amount
    validate_transaction_amount(amount)
    
    # Check daily limit
    check_daily_transaction_limit(db, user_id, wallet_id, amount)
