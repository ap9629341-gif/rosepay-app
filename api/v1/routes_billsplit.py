"""
Bill Split API routes.

WHAT THIS FILE DOES:
- Handles bill splitting
- Creates bill splits
- Settles participant shares
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from core.security import get_current_user
from models import User
from schemas import BillSplitCreate, BillSplitResponse
from services.bill_split_service import (
    create_bill_split,
    get_user_bill_splits,
    settle_bill_participant
)

router = APIRouter()


@router.post("/create", response_model=BillSplitResponse, summary="Create bill split")
def create_bill(
    request: BillSplitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a bill split.
    
    WHAT IT DOES:
    1. Creates bill split record
    2. Adds participants
    3. Validates amounts
    4. Returns bill split
    
    EXAMPLE:
    Restaurant bill: $100
    Split among 3 people:
    - Person 1: $40
    - Person 2: $30
    - Person 3: $30
    """
    return create_bill_split(
        db,
        current_user.id,
        request.title,
        request.total_amount,
        request.description,
        request.participants,
        request.currency
    )


@router.get("/list", response_model=list[BillSplitResponse], summary="Get my bill splits")
def list_bills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all bill splits where you're creator or participant.
    """
    return get_user_bill_splits(db, current_user.id)


@router.post("/{bill_split_id}/settle/{participant_id}", summary="Settle bill share")
def settle_share(
    bill_split_id: int,
    participant_id: int,
    wallet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Pay your share of a bill split.
    
    WHAT IT DOES:
    1. Transfers money to bill creator
    2. Marks your share as paid
    3. Updates bill status if all paid
    """
    from schemas import TransactionResponse
    from models import Transaction
    
    transaction = settle_bill_participant(
        db,
        bill_split_id,
        participant_id,
        current_user.id,
        wallet_id
    )
    
    # Convert to response
    return {
        "id": transaction.id,
        "user_id": transaction.user_id,
        "wallet_id": transaction.wallet_id,
        "amount": transaction.amount,
        "transaction_type": transaction.transaction_type,
        "status": transaction.status,
        "description": transaction.description,
        "recipient_wallet_id": transaction.recipient_wallet_id,
        "created_at": transaction.created_at
    }
