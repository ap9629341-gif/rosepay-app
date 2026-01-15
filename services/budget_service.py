"""
Budget Service

WHAT THIS FILE DOES:
- Manages spending budgets
- Tracks spending against budgets
- Provides budget alerts

LEARN:
- Budget = Spending limit
- Helps control expenses
- Tracks progress
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from models import Budget, Wallet, Transaction, TransactionStatus, TransactionType
from schemas import BudgetCreate


def create_budget(
    db: Session,
    user_id: int,
    request: BudgetCreate
) -> Budget:
    """
    Create a new budget.
    
    WHAT IT DOES:
    1. Validates wallet (if specified)
    2. Calculates period start
    3. Creates budget record
    4. Returns the budget
    """
    # Validate wallet if specified
    if request.wallet_id:
        from services.wallet_service import get_wallet
        get_wallet(db, request.wallet_id, user_id)
    
    # Calculate period start based on period type
    period_start = datetime.utcnow()
    if request.period == "daily":
        period_start = period_start.replace(hour=0, minute=0, second=0, microsecond=0)
    elif request.period == "weekly":
        # Start of week (Monday)
        days_since_monday = period_start.weekday()
        period_start = period_start - timedelta(days=days_since_monday)
        period_start = period_start.replace(hour=0, minute=0, second=0, microsecond=0)
    elif request.period == "monthly":
        period_start = period_start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Create budget
    budget = Budget(
        user_id=user_id,
        wallet_id=request.wallet_id,
        category=request.category,
        amount=request.amount,
        period=request.period,
        current_spent=0.0,
        period_start=period_start,
        is_active=1
    )
    
    db.add(budget)
    db.commit()
    db.refresh(budget)
    
    return budget


def get_user_budgets(
    db: Session,
    user_id: int,
    active_only: bool = True
) -> list[Budget]:
    """Get all budgets for a user."""
    query = db.query(Budget).filter(Budget.user_id == user_id)
    
    if active_only:
        query = query.filter(Budget.is_active == 1)
    
    budgets = query.all()
    
    # Calculate current spending for each budget
    for budget in budgets:
        update_budget_spending(db, budget)
    
    return budgets


def update_budget_spending(db: Session, budget: Budget) -> None:
    """
    Update budget's current spending.
    
    WHAT IT DOES:
    1. Calculates period end date
    2. Gets all transactions in period
    3. Sums up spending
    4. Updates budget
    """
    # Calculate period end
    period_end = datetime.utcnow()
    if budget.period == "daily":
        period_end = budget.period_start + timedelta(days=1)
    elif budget.period == "weekly":
        period_end = budget.period_start + timedelta(weeks=1)
    elif budget.period == "monthly":
        # Next month
        if budget.period_start.month == 12:
            period_end = budget.period_start.replace(year=budget.period_start.year + 1, month=1)
        else:
            period_end = budget.period_start.replace(month=budget.period_start.month + 1)
    
    # Get transactions in period
    query = db.query(Transaction).filter(
        Transaction.user_id == budget.user_id,
        Transaction.status == TransactionStatus.COMPLETED,
        Transaction.created_at >= budget.period_start,
        Transaction.created_at < period_end
    )
    
    # Filter by wallet if specified
    if budget.wallet_id:
        query = query.filter(Transaction.wallet_id == budget.wallet_id)
    
    # Filter by category if specified (would need category field in transactions)
    # For now, we'll track all spending
    
    # Sum spending (only withdrawals, transfers, payments - not deposits)
    transactions = query.filter(
        Transaction.transaction_type.in_([
            TransactionType.WITHDRAWAL,
            TransactionType.TRANSFER,
            TransactionType.PAYMENT
        ])
    ).all()
    
    total_spent = sum(t.amount for t in transactions)
    
    # Update budget
    budget.current_spent = total_spent
    
    # Check if period has passed, reset if needed
    if datetime.utcnow() >= period_end:
        # Reset for new period
        budget.period_start = period_end
        budget.current_spent = 0.0
    
    db.commit()


def check_budget_exceeded(
    db: Session,
    user_id: int,
    wallet_id: int,
    amount: float
) -> list[Budget]:
    """
    Check if a transaction would exceed any budgets.
    
    WHAT IT DOES:
    1. Gets all active budgets for user/wallet
    2. Calculates if transaction would exceed budget
    3. Returns list of exceeded budgets
    
    USAGE:
    Call before processing transactions to warn user
    """
    budgets = get_user_budgets(db, user_id, active_only=True)
    
    # Filter by wallet if specified
    relevant_budgets = [
        b for b in budgets
        if b.wallet_id is None or b.wallet_id == wallet_id
    ]
    
    exceeded = []
    for budget in relevant_budgets:
        update_budget_spending(db, budget)
        if budget.current_spent + amount > budget.amount:
            exceeded.append(budget)
    
    return exceeded
