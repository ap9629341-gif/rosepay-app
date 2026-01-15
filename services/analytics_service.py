"""
Analytics and statistics service.

WHAT THIS FILE DOES:
- Calculate transaction statistics
- Generate reports (daily, weekly, monthly)
- Track spending patterns
- Revenue analytics

LEARN:
- Analytics = analyzing data to understand patterns
- Helps users see spending habits
- Helps merchants see revenue trends
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from models import Transaction, TransactionStatus, TransactionType


def get_user_transaction_stats(
    db: Session,
    user_id: int,
    wallet_id: Optional[int] = None,
    days: int = 30
) -> dict:
    """
    Get transaction statistics for a user.
    
    WHAT IT DOES:
    1. Gets all transactions in last N days
    2. Calculates totals by type
    3. Returns statistics
    
    EXAMPLE OUTPUT:
    {
        "total_deposits": 1000.0,
        "total_withdrawals": 200.0,
        "total_transfers": 300.0,
        "transaction_count": 15
    }
    """
    # Calculate date range
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Build query
    query = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.status == TransactionStatus.COMPLETED,
        Transaction.created_at >= start_date
    )
    
    # Filter by wallet if provided
    if wallet_id:
        query = query.filter(Transaction.wallet_id == wallet_id)
    
    transactions = query.all()
    
    # Calculate statistics
    stats = {
        "period_days": days,
        "total_deposits": 0.0,
        "total_withdrawals": 0.0,
        "total_transfers": 0.0,
        "total_payments": 0.0,
        "transaction_count": len(transactions),
        "average_transaction": 0.0
    }
    
    total_amount = 0.0
    
    for transaction in transactions:
        amount = transaction.amount
        total_amount += amount
        
        if transaction.transaction_type == TransactionType.DEPOSIT:
            stats["total_deposits"] += amount
        elif transaction.transaction_type == TransactionType.WITHDRAWAL:
            stats["total_withdrawals"] += amount
        elif transaction.transaction_type == TransactionType.TRANSFER:
            stats["total_transfers"] += amount
        elif transaction.transaction_type == TransactionType.PAYMENT:
            stats["total_payments"] += amount
    
    # Calculate average
    if stats["transaction_count"] > 0:
        stats["average_transaction"] = total_amount / stats["transaction_count"]
    
    return stats


def get_daily_transaction_summary(
    db: Session,
    user_id: int,
    wallet_id: Optional[int] = None,
    date: Optional[datetime] = None
) -> dict:
    """
    Get daily transaction summary.
    
    WHAT IT DOES:
    1. Gets all transactions for a specific day
    2. Groups by type
    3. Returns summary
    """
    if not date:
        date = datetime.utcnow()
    
    # Get start and end of day
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    query = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.status == TransactionStatus.COMPLETED,
        Transaction.created_at >= start_of_day,
        Transaction.created_at <= end_of_day
    )
    
    if wallet_id:
        query = query.filter(Transaction.wallet_id == wallet_id)
    
    transactions = query.all()
    
    return {
        "date": date.date().isoformat(),
        "transaction_count": len(transactions),
        "total_amount": sum(t.amount for t in transactions),
        "transactions": [
            {
                "id": t.id,
                "type": t.transaction_type.value,
                "amount": t.amount,
                "description": t.description,
                "time": t.created_at.isoformat()
            }
            for t in transactions
        ]
    }


def get_spending_by_category(
    db: Session,
    user_id: int,
    days: int = 30
) -> dict:
    """
    Get spending breakdown by transaction type.
    
    WHAT IT DOES:
    1. Groups transactions by type
    2. Calculates totals
    3. Returns breakdown
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.status == TransactionStatus.COMPLETED,
        Transaction.created_at >= start_date
    ).all()
    
    breakdown = {
        "deposits": 0.0,
        "withdrawals": 0.0,
        "transfers": 0.0,
        "payments": 0.0
    }
    
    for transaction in transactions:
        amount = transaction.amount
        transaction_type = transaction.transaction_type.value
        
        if transaction_type in breakdown:
            breakdown[transaction_type] += amount
    
    return breakdown
