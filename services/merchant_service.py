"""
Merchant service - for businesses/vendors.

WHAT THIS FILE DOES:
- Allows users to become merchants (like shops, restaurants)
- Merchants can receive payments
- Track merchant revenue
- Generate merchant reports

LEARN:
- Merchants = businesses that accept payments
- Like Google Pay merchants, PhonePe merchants
- Merchants have unique IDs for payments
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import secrets
import string

from models import Merchant, User


def generate_merchant_id() -> str:
    """
    Generate unique merchant ID.
    
    WHAT IT DOES:
    1. Creates random string (like "MRCH_ABC123")
    2. Ensures uniqueness
    3. Returns merchant ID
    
    EXAMPLE:
    "MRCH_X7K9M2P"
    """
    # Generate random 8-character ID
    chars = string.ascii_uppercase + string.digits
    random_id = ''.join(secrets.choice(chars) for _ in range(8))
    return f"MRCH_{random_id}"


def create_merchant(
    db: Session,
    user_id: int,
    business_name: str,
    business_type: str = None
) -> Merchant:
    """
    Create a merchant account for a user.
    
    WHAT IT DOES:
    1. Checks if user already has merchant account
    2. Generates unique merchant ID
    3. Creates merchant record
    4. Returns merchant
    
    EXAMPLE:
    User registers as "Pizza Shop" → Gets merchant ID "MRCH_ABC123"
    """
    # Check if user already has merchant account
    existing = db.query(Merchant).filter(Merchant.user_id == user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a merchant account"
        )
    
    # Generate unique merchant ID
    merchant_id = generate_merchant_id()
    
    # Ensure uniqueness
    while db.query(Merchant).filter(Merchant.merchant_id == merchant_id).first():
        merchant_id = generate_merchant_id()
    
    # Create merchant
    merchant = Merchant(
        user_id=user_id,
        business_name=business_name,
        business_type=business_type,
        merchant_id=merchant_id,
        is_active=1,
        total_revenue=0.0
    )
    
    db.add(merchant)
    db.commit()
    db.refresh(merchant)
    
    return merchant


def get_merchant(db: Session, merchant_id: str) -> Merchant:
    """Get merchant by merchant ID."""
    merchant = db.query(Merchant).filter(
        Merchant.merchant_id == merchant_id,
        Merchant.is_active == 1
    ).first()
    
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant not found"
        )
    
    return merchant


def get_user_merchant(db: Session, user_id: int) -> Merchant:
    """Get merchant account for a user."""
    merchant = db.query(Merchant).filter(Merchant.user_id == user_id).first()
    
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Merchant account not found"
        )
    
    return merchant


def update_merchant_revenue(
    db: Session,
    merchant_id: str,
    amount: float
) -> None:
    """
    Update merchant total revenue.
    
    WHAT IT DOES:
    1. Gets merchant
    2. Adds amount to total_revenue
    3. Saves to database
    
    USAGE:
    Call this when merchant receives payment
    """
    merchant = get_merchant(db, merchant_id)
    merchant.total_revenue += amount
    db.commit()


def get_merchant_stats(db: Session, user_id: int) -> dict:
    """
    Get merchant statistics.
    
    WHAT IT DOES:
    1. Gets merchant account
    2. Returns stats (revenue, etc.)
    """
    merchant = get_user_merchant(db, user_id)
    
    # Get transaction count
    from models import Transaction, TransactionStatus, Wallet
    # Get merchant's wallet
    merchant_wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if merchant_wallet:
        transaction_count = db.query(Transaction).filter(
            Transaction.recipient_wallet_id == merchant_wallet.id,
            Transaction.status == TransactionStatus.COMPLETED
        ).count()
    else:
        transaction_count = 0
    
    return {
        "merchant_id": merchant.merchant_id,
        "business_name": merchant.business_name,
        "business_type": merchant.business_type,
        "total_revenue": merchant.total_revenue,
        "transaction_count": transaction_count,
        "is_active": bool(merchant.is_active)
    }
