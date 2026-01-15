"""
Payment link service - create and manage payment links (like PayTM links).
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import secrets
import string

from models import PaymentLink, Transaction, TransactionType, TransactionStatus, Wallet
from schemas import AddMoneyRequest


def generate_link_id() -> str:
    """Generate a unique payment link ID."""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))


def create_payment_link(
    db: Session,
    user_id: int,
    amount: float,
    description: str = None,
    expires_hours: int = 24
) -> PaymentLink:
    """
    Create a payment link.
    
    WHAT IT DOES:
    1. Generates unique link ID
    2. Creates payment link record
    3. Returns link that can be shared
    """
    link_id = generate_link_id()
    
    # Check if link_id already exists (very rare, but check anyway)
    while db.query(PaymentLink).filter(PaymentLink.link_id == link_id).first():
        link_id = generate_link_id()
    
    expires_at = datetime.utcnow() + timedelta(hours=expires_hours) if expires_hours else None
    
    payment_link = PaymentLink(
        user_id=user_id,
        link_id=link_id,
        amount=amount,
        description=description,
        expires_at=expires_at
    )
    
    db.add(payment_link)
    db.commit()
    db.refresh(payment_link)
    
    return payment_link


def get_payment_link(db: Session, link_id: str) -> PaymentLink:
    """Get payment link by link_id."""
    payment_link = db.query(PaymentLink).filter(PaymentLink.link_id == link_id).first()
    
    if not payment_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment link not found"
        )
    
    if not payment_link.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment link has already been used"
        )
    
    if payment_link.expires_at and payment_link.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment link has expired"
        )
    
    return payment_link


def pay_via_link(
    db: Session,
    link_id: str,
    payer_wallet_id: int,
    payer_user_id: int
) -> Transaction:
    """
    Pay via payment link.
    
    WHAT IT DOES:
    1. Get payment link
    2. Check payer has enough balance
    3. Transfer money to link creator
    4. Mark link as used
    5. Create transaction
    """
    payment_link = get_payment_link(db, link_id)
    
    # Can't pay your own link
    if payment_link.user_id == payer_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot pay your own payment link"
        )
    
    # Get payer wallet
    payer_wallet = db.query(Wallet).filter(
        Wallet.id == payer_wallet_id,
        Wallet.user_id == payer_user_id
    ).first()
    
    if not payer_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payer wallet not found"
        )
    
    # Check balance
    if payer_wallet.balance < payment_link.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )
    
    # Get recipient wallet (link creator's default wallet)
    recipient_wallet = db.query(Wallet).filter(
        Wallet.user_id == payment_link.user_id
    ).first()
    
    if not recipient_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient wallet not found"
        )
    
    # Transfer money
    payer_wallet.balance -= payment_link.amount
    recipient_wallet.balance += payment_link.amount
    
    # Create transaction
    transaction = Transaction(
        user_id=payer_user_id,
        wallet_id=payer_wallet_id,
        amount=payment_link.amount,
        transaction_type=TransactionType.PAYMENT,
        status=TransactionStatus.COMPLETED,
        description=payment_link.description or f"Payment via link {link_id}",
        recipient_wallet_id=recipient_wallet.id
    )
    
    # Mark link as used
    payment_link.is_active = 0
    payment_link.paid_at = datetime.utcnow()
    payment_link.transaction_id = transaction.id
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction
