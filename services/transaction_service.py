"""
Transaction service - handles transaction history.
"""
from sqlalchemy.orm import Session
from typing import List

from models import Transaction, Wallet


def get_user_transactions(
    db: Session,
    user_id: int,
    wallet_id: int = None,
    limit: int = 50
) -> List[Transaction]:
    """
    Get transaction history for a user.
    
    WHAT IT DOES:
    1. Get all transactions for a user
    2. Optionally filter by wallet
    3. Return recent transactions
    """
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    
    # Filter by wallet if provided
    if wallet_id:
        # Verify user owns the wallet
        wallet = db.query(Wallet).filter(
            Wallet.id == wallet_id,
            Wallet.user_id == user_id
        ).first()
        
        if not wallet:
            return []
        
        query = query.filter(Transaction.wallet_id == wallet_id)
    
    # Get recent transactions, ordered by newest first
    transactions = query.order_by(Transaction.created_at.desc()).limit(limit).all()
    
    return transactions


def get_transaction_by_id(
    db: Session,
    transaction_id: int,
    user_id: int
) -> Transaction:
    """Get a specific transaction (only if user owns it)."""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id
    ).first()
    
    if not transaction:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction
