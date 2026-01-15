"""
Transaction routes - transaction history endpoints.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from schemas import TransactionResponse
from services.transaction_service import get_user_transactions, get_transaction_by_id
from core.security import get_current_user
from models import User

router = APIRouter()


@router.get("/", response_model=List[TransactionResponse], summary="Get transaction history")
def list_transactions(
    wallet_id: Optional[int] = Query(None, description="Filter by wallet ID"),
    limit: int = Query(50, description="Number of transactions to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get transaction history for the current user.
    
    WHAT IT DOES:
    1. Gets all transactions for logged-in user
    2. Optionally filters by wallet
    3. Returns recent transactions
    """
    return get_user_transactions(db, current_user.id, wallet_id, limit)


@router.get("/{transaction_id}", response_model=TransactionResponse, summary="Get transaction details")
def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific transaction.
    """
    return get_transaction_by_id(db, transaction_id, current_user.id)
