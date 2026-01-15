"""
Payment Gateway routes - Razorpay integration.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    CreateGatewayOrderRequest, GatewayOrderResponse,
    VerifyPaymentRequest, TransactionResponse, PaymentStatusResponse
)
from services.payment_gateway_service import (
    create_razorpay_order,
    add_money_via_gateway,
    get_payment_status
)
from core.security import get_current_user
from models import User
from config import settings

router = APIRouter()


@router.post("/order/create", response_model=GatewayOrderResponse, summary="Create payment order")
def create_order(
    order_data: CreateGatewayOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a Razorpay payment order.
    
    WHAT IT DOES:
    1. Creates an order in Razorpay
    2. Returns order_id and key_id
    3. Frontend uses this to process payment
    4. After payment, call /verify endpoint
    """
    # Create order in Razorpay
    order = create_razorpay_order(
        amount=order_data.amount,
        currency=order_data.currency,
        notes={
            "user_id": str(current_user.id),
            "description": order_data.description or "Wallet top-up"
        }
    )
    
    return GatewayOrderResponse(
        order_id=order["id"],
        amount=order_data.amount,
        currency=order_data.currency,
        key_id=settings.RAZORPAY_KEY_ID,
        receipt=order["receipt"]
    )


@router.post("/verify", response_model=TransactionResponse, summary="Verify and complete payment")
def verify_payment(
    payment_data: VerifyPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify payment and add money to wallet.
    
    WHAT IT DOES:
    1. Verifies payment signature from Razorpay
    2. Confirms payment was successful
    3. Adds money to user's wallet
    4. Creates transaction record
    
    IMPORTANT: Call this after Razorpay payment succeeds!
    """
    transaction = add_money_via_gateway(
        db=db,
        wallet_id=payment_data.wallet_id,
        user_id=current_user.id,
        amount=payment_data.amount,
        razorpay_order_id=payment_data.razorpay_order_id,
        razorpay_payment_id=payment_data.razorpay_payment_id,
        razorpay_signature=payment_data.razorpay_signature,
        description=payment_data.description
    )
    
    return TransactionResponse(
        id=transaction.id,
        user_id=transaction.user_id,
        wallet_id=transaction.wallet_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        status=transaction.status,
        description=transaction.description,
        recipient_wallet_id=transaction.recipient_wallet_id,
        created_at=transaction.created_at
    )


@router.get("/status/{payment_id}", response_model=PaymentStatusResponse, summary="Check payment status")
def check_payment_status(
    payment_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Check payment status from Razorpay.
    
    WHAT IT DOES:
    1. Fetches payment details from Razorpay
    2. Returns payment status
    """
    payment_info = get_payment_status(payment_id)
    
    return PaymentStatusResponse(
        payment_id=payment_info["payment_id"],
        status=payment_info["status"],
        amount=payment_info["amount"],
        currency=payment_info["currency"],
        method=payment_info["method"]
    )


@router.post("/webhook", summary="Razorpay webhook endpoint")
async def razorpay_webhook(request: dict):
    """
    Razorpay webhook endpoint.
    
    WHAT IT DOES:
    1. Receives payment events from Razorpay
    2. Updates transaction status
    3. Handles payment.success, payment.failed, etc.
    
    NOTE: Configure this URL in Razorpay dashboard webhooks section.
    """
    # TODO: Implement webhook handler
    # Verify webhook signature
    # Handle different event types (payment.success, payment.failed, etc.)
    # Update transaction status accordingly
    
    return {"status": "received"}
