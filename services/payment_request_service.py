"""
Payment request service - request money from other users.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from models import PaymentRequest, Transaction, TransactionType, TransactionStatus, Wallet


def create_payment_request(
    db: Session,
    requester_id: int,
    recipient_email: str,
    amount: float,
    description: str = None
) -> PaymentRequest:
    """
    Create a payment request (request money from someone).
    
    WHAT IT DOES:
    1. Find recipient by email
    2. Create payment request
    3. Recipient can accept/reject later
    """
    from models import User
    
    # Find recipient by email
    recipient = db.query(User).filter(User.email == recipient_email).first()
    
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )
    
    if requester_id == recipient.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot request money from yourself"
        )
    
    payment_request = PaymentRequest(
        requester_id=requester_id,
        recipient_id=recipient.id,
        amount=amount,
        description=description
    )
    
    db.add(payment_request)
    db.commit()
    db.refresh(payment_request)
    
    return payment_request


def get_payment_requests(
    db: Session,
    user_id: int,
    request_type: str = "received"  # "received" or "sent"
) -> list[PaymentRequest]:
    """
    Get payment requests.
    - received: Requests where user should pay
    - sent: Requests user sent to others
    """
    if request_type == "received":
        return db.query(PaymentRequest).filter(
            PaymentRequest.recipient_id == user_id,
            PaymentRequest.status == TransactionStatus.PENDING
        ).all()
    else:
        return db.query(PaymentRequest).filter(
            PaymentRequest.requester_id == user_id
        ).all()


def accept_payment_request(
    db: Session,
    request_id: int,
    payer_wallet_id: int,
    payer_user_id: int
) -> Transaction:
    """
    Accept and pay a payment request.
    
    WHAT IT DOES:
    1. Get payment request
    2. Verify payer is the recipient
    3. Check balance
    4. Transfer money
    5. Mark request as completed
    """
    payment_request = db.query(PaymentRequest).filter(
        PaymentRequest.id == request_id
    ).first()
    
    if not payment_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment request not found"
        )
    
    if payment_request.recipient_id != payer_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to pay this request"
        )
    
    if payment_request.status != TransactionStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment request already processed"
        )
    
    # Get payer wallet
    payer_wallet = db.query(Wallet).filter(
        Wallet.id == payer_wallet_id,
        Wallet.user_id == payer_user_id
    ).first()
    
    if not payer_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    
    # Check balance
    if payer_wallet.balance < payment_request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )
    
    # Get requester wallet
    requester_wallet = db.query(Wallet).filter(
        Wallet.user_id == payment_request.requester_id
    ).first()
    
    if not requester_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requester wallet not found"
        )
    
    # Transfer money
    payer_wallet.balance -= payment_request.amount
    requester_wallet.balance += payment_request.amount
    
    # Create transaction
    transaction = Transaction(
        user_id=payer_user_id,
        wallet_id=payer_wallet_id,
        amount=payment_request.amount,
        transaction_type=TransactionType.PAYMENT,
        status=TransactionStatus.COMPLETED,
        description=payment_request.description or "Payment request",
        recipient_wallet_id=requester_wallet.id
    )
    
    # Update payment request
    payment_request.status = TransactionStatus.COMPLETED
    payment_request.paid_at = datetime.utcnow()
    payment_request.transaction_id = transaction.id
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction
