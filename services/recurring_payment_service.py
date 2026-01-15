"""
Recurring Payment Service

WHAT THIS FILE DOES:
- Manages recurring payments (subscriptions, automatic transfers)
- Handles payment scheduling
- Processes recurring payments automatically

LEARN:
- Recurring payments = Automatic payments on schedule
- Like Netflix subscription, monthly rent, etc.
- Cron jobs would process these in production
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from models import RecurringPayment, Wallet, Transaction, TransactionType, TransactionStatus
from schemas import RecurringPaymentCreate


def calculate_next_payment_date(frequency: str, current_date: datetime = None) -> datetime:
    """
    Calculate next payment date based on frequency.
    
    WHAT IT DOES:
    1. Takes frequency (daily, weekly, monthly, yearly)
    2. Calculates next payment date
    3. Returns the date
    
    EXAMPLE:
    - daily → next day
    - weekly → next week
    - monthly → next month
    """
    if not current_date:
        current_date = datetime.utcnow()
    
    if frequency == "daily":
        return current_date + timedelta(days=1)
    elif frequency == "weekly":
        return current_date + timedelta(weeks=1)
    elif frequency == "monthly":
        # Add approximately 30 days (simplified)
        return current_date + timedelta(days=30)
    elif frequency == "yearly":
        return current_date + timedelta(days=365)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid frequency: {frequency}. Must be: daily, weekly, monthly, yearly"
        )


def create_recurring_payment(
    db: Session,
    user_id: int,
    request: RecurringPaymentCreate
) -> RecurringPayment:
    """
    Create a new recurring payment.
    
    WHAT IT DOES:
    1. Validates wallet ownership
    2. Calculates next payment date
    3. Creates recurring payment record
    4. Returns the recurring payment
    """
    from services.wallet_service import get_wallet
    
    # Validate wallet
    wallet = get_wallet(db, request.wallet_id, user_id)
    
    # Calculate next payment date
    next_payment = calculate_next_payment_date(request.frequency)
    
    # Create recurring payment
    recurring = RecurringPayment(
        user_id=user_id,
        wallet_id=request.wallet_id,
        recipient_wallet_id=request.recipient_wallet_id,
        recipient_email=request.recipient_email,
        amount=request.amount,
        description=request.description,
        frequency=request.frequency,
        next_payment_date=next_payment,
        end_date=request.end_date,
        is_active=1,
        total_payments=0
    )
    
    db.add(recurring)
    db.commit()
    db.refresh(recurring)
    
    return recurring


def get_user_recurring_payments(
    db: Session,
    user_id: int,
    active_only: bool = True
) -> list[RecurringPayment]:
    """Get all recurring payments for a user."""
    query = db.query(RecurringPayment).filter(RecurringPayment.user_id == user_id)
    
    if active_only:
        query = query.filter(RecurringPayment.is_active == 1)
    
    return query.all()


def process_recurring_payment(
    db: Session,
    recurring_id: int
) -> Transaction:
    """
    Process a recurring payment (execute it).
    
    WHAT IT DOES:
    1. Gets recurring payment
    2. Checks if it's due
    3. Executes the payment
    4. Updates next payment date
    5. Creates transaction record
    
    NOTE: In production, this would be called by a cron job/scheduler
    """
    recurring = db.query(RecurringPayment).filter(
        RecurringPayment.id == recurring_id,
        RecurringPayment.is_active == 1
    ).first()
    
    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring payment not found"
        )
    
    # Check if payment is due
    if datetime.utcnow() < recurring.next_payment_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment not due yet"
        )
    
    # Check if ended
    if recurring.end_date and datetime.utcnow() > recurring.end_date:
        recurring.is_active = 0
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recurring payment has ended"
        )
    
    # Get wallet
    wallet = db.query(Wallet).filter(Wallet.id == recurring.wallet_id).first()
    
    # Process payment based on type
    if recurring.recipient_wallet_id:
        # Transfer to another wallet
        from services.wallet_service import transfer_money
        from schemas import TransferRequest
        
        transfer_request = TransferRequest(
            recipient_wallet_id=recurring.recipient_wallet_id,
            amount=recurring.amount,
            description=recurring.description or f"Recurring payment ({recurring.frequency})"
        )
        
        transaction = transfer_money(
            db,
            recurring.wallet_id,
            recurring.user_id,
            transfer_request
        )
    else:
        # Payment request (would need recipient_email handling)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment requests not yet supported in recurring payments"
        )
    
    # Update recurring payment
    recurring.last_paid_at = datetime.utcnow()
    recurring.total_payments += 1
    recurring.next_payment_date = calculate_next_payment_date(
        recurring.frequency,
        recurring.next_payment_date
    )
    
    db.commit()
    db.refresh(recurring)
    
    return transaction


def cancel_recurring_payment(
    db: Session,
    recurring_id: int,
    user_id: int
) -> RecurringPayment:
    """Cancel a recurring payment."""
    recurring = db.query(RecurringPayment).filter(
        RecurringPayment.id == recurring_id,
        RecurringPayment.user_id == user_id
    ).first()
    
    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring payment not found"
        )
    
    recurring.is_active = 0
    db.commit()
    db.refresh(recurring)
    
    return recurring
