"""
Payment Gateway Service - Razorpay integration.
"""
import razorpay
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from config import settings
from models import Transaction, Wallet, TransactionType, TransactionStatus


# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(
    amount: float,
    currency: str = "INR",
    receipt: str = None,
    notes: dict = None
) -> dict:
    """
    Create a Razorpay order.
    
    WHAT IT DOES:
    1. Creates an order in Razorpay
    2. Returns order details with order_id
    3. User can pay using this order_id
    """
    try:
        # Convert amount to paise (Razorpay uses smallest currency unit)
        amount_in_paise = int(amount * 100)
        
        order_data = {
            "amount": amount_in_paise,
            "currency": currency,
            "receipt": receipt or f"receipt_{datetime.utcnow().timestamp()}",
            "notes": notes or {}
        }
        
        order = client.order.create(data=order_data)
        return order
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create order: {str(e)}"
        )


def verify_payment_signature(
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str
) -> bool:
    """
    Verify Razorpay payment signature.
    
    WHAT IT DOES:
    1. Verifies that payment came from Razorpay
    2. Prevents payment fraud
    3. Returns True if signature is valid
    """
    try:
        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        }
        
        client.utility.verify_payment_signature(params_dict)
        return True
        
    except razorpay.errors.SignatureVerificationError:
        return False
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment verification failed: {str(e)}"
        )


def capture_payment(
    razorpay_payment_id: str,
    amount: float,
    currency: str = "INR"
) -> dict:
    """
    Capture a payment (for manual capture mode).
    Usually not needed as auto-capture is default.
    """
    try:
        amount_in_paise = int(amount * 100)
        
        payment = client.payment.capture(razorpay_payment_id, amount_in_paise)
        return payment
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment capture failed: {str(e)}"
        )


def add_money_via_gateway(
    db: Session,
    wallet_id: int,
    user_id: int,
    amount: float,
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
    description: str = None
) -> Transaction:
    """
    Add money to wallet via Razorpay gateway.
    
    WHAT IT DOES:
    1. Verify payment signature
    2. Verify payment succeeded
    3. Add money to wallet
    4. Create transaction record
    """
    from services.wallet_service import get_wallet
    
    # Verify payment signature
    if not verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment signature"
        )
    
    # Get wallet
    wallet = get_wallet(db, wallet_id, user_id)
    
    # Get payment details from Razorpay
    try:
        payment = client.payment.fetch(razorpay_payment_id)
        
        if payment["status"] != "captured" and payment["status"] != "authorized":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment not successful. Status: {payment['status']}"
            )
        
        # Verify amount matches
        amount_paid = payment["amount"] / 100  # Convert from paise to rupees
        if abs(amount_paid - amount) > 0.01:  # Allow small rounding differences
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount mismatch"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to verify payment: {str(e)}"
        )
    
    # Add money to wallet
    wallet.balance += amount
    
    # Create transaction record
    transaction = Transaction(
        user_id=user_id,
        wallet_id=wallet_id,
        amount=amount,
        transaction_type=TransactionType.DEPOSIT,
        status=TransactionStatus.COMPLETED,
        description=description or f"Razorpay payment - Order: {razorpay_order_id}"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction


def get_payment_status(razorpay_payment_id: str) -> dict:
    """
    Get payment status from Razorpay.
    """
    try:
        payment = client.payment.fetch(razorpay_payment_id)
        return {
            "payment_id": payment["id"],
            "status": payment["status"],
            "amount": payment["amount"] / 100,
            "currency": payment["currency"],
            "method": payment.get("method", "unknown")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch payment: {str(e)}"
        )
