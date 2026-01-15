"""
Bill Split Service

WHAT THIS FILE DOES:
- Manages bill splitting with friends
- Tracks who owes what
- Handles settlement of bills

LEARN:
- Bill splitting = Dividing expenses among people
- Like splitting restaurant bill, rent, etc.
- Each person pays their share
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from models import BillSplit, BillSplitParticipant, User, Wallet, Transaction, TransactionType, TransactionStatus


def create_bill_split(
    db: Session,
    creator_id: int,
    title: str,
    total_amount: float,
    description: str,
    participants_data: list[dict],
    currency: str = "USD"
) -> BillSplit:
    """
    Create a bill split.
    
    WHAT IT DOES:
    1. Creates bill split record
    2. Creates participant records
    3. Validates amounts add up
    4. Returns the bill split
    
    EXAMPLE:
    Bill: $100
    Participants:
    - User 1: $40
    - User 2: $30
    - User 3: $30
    Total: $100 ✅
    """
    # Validate total matches participants
    total_owed = sum(p.get('amount', 0) for p in participants_data)
    
    if abs(total_owed - total_amount) > 0.01:  # Allow small floating point differences
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Participant amounts (${total_owed:.2f}) don't match total (${total_amount:.2f})"
        )
    
    # Create bill split
    bill_split = BillSplit(
        creator_id=creator_id,
        title=title,
        description=description,
        total_amount=total_amount,
        currency=currency,
        status=TransactionStatus.PENDING
    )
    
    db.add(bill_split)
    db.flush()  # Get the ID
    
    # Create participants
    for participant_data in participants_data:
        user_id = participant_data.get('user_id')
        amount = participant_data.get('amount', 0)
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found"
            )
        
        participant = BillSplitParticipant(
            bill_split_id=bill_split.id,
            user_id=user_id,
            amount_owed=amount,
            amount_paid=0.0,
            is_settled=0
        )
        
        db.add(participant)
    
    db.commit()
    db.refresh(bill_split)
    
    return bill_split


def get_user_bill_splits(
    db: Session,
    user_id: int
) -> list[BillSplit]:
    """Get all bill splits where user is creator or participant."""
    # As creator
    created = db.query(BillSplit).filter(BillSplit.creator_id == user_id).all()
    
    # As participant
    participant_ids = db.query(BillSplitParticipant.bill_split_id).filter(
        BillSplitParticipant.user_id == user_id
    ).all()
    participant_ids = [p[0] for p in participant_ids]
    
    participated = db.query(BillSplit).filter(
        BillSplit.id.in_(participant_ids)
    ).all() if participant_ids else []
    
    # Combine and remove duplicates
    all_splits = {split.id: split for split in created + participated}
    return list(all_splits.values())


def settle_bill_participant(
    db: Session,
    bill_split_id: int,
    participant_id: int,
    user_id: int,
    wallet_id: int
):
    """
    Settle a participant's share of a bill.
    
    WHAT IT DOES:
    1. Gets participant record
    2. Validates user owns the participant record
    3. Processes payment
    4. Marks as settled
    """
    from services.wallet_service import transfer_money
    from schemas import TransferRequest
    
    # Get participant
    participant = db.query(BillSplitParticipant).filter(
        BillSplitParticipant.id == participant_id,
        BillSplitParticipant.user_id == user_id,
        BillSplitParticipant.bill_split_id == bill_split_id
    ).first()
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found or you don't have permission"
        )
    
    if participant.is_settled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This share is already settled"
        )
    
    # Get bill split
    bill_split = db.query(BillSplit).filter(BillSplit.id == bill_split_id).first()
    
    # Get creator's wallet (to send money to)
    creator_wallet = db.query(Wallet).filter(
        Wallet.user_id == bill_split.creator_id
    ).first()
    
    if not creator_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator wallet not found"
        )
    
    # Transfer money
    transfer_request = TransferRequest(
        recipient_wallet_id=creator_wallet.id,
        amount=participant.amount_owed,
        description=f"Bill split: {bill_split.title}"
    )
    
    transaction = transfer_money(
        db,
        wallet_id,
        user_id,
        transfer_request
    )
    
    # Update participant
    participant.amount_paid = participant.amount_owed
    participant.is_settled = 1
    participant.settled_at = datetime.utcnow()
    participant.transaction_id = transaction.id
    
    # Check if all participants are settled
    remaining = db.query(BillSplitParticipant).filter(
        BillSplitParticipant.bill_split_id == bill_split_id,
        BillSplitParticipant.is_settled == 0
    ).count()
    
    if remaining == 0:
        bill_split.status = TransactionStatus.COMPLETED
        bill_split.settled_at = datetime.utcnow()
    
    db.commit()
    db.refresh(participant)
    
    return transaction
