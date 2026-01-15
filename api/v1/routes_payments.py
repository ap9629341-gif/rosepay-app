"""
Payment routes - payment links, QR codes, payment requests.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import (
    PaymentLinkCreate, PaymentLinkResponse, PayLinkRequest,
    PaymentRequestCreate, PaymentRequestResponse, AcceptPaymentRequest,
    QRCodeResponse, TransactionResponse
)
from services.payment_link_service import create_payment_link, get_payment_link, pay_via_link
from services.payment_request_service import (
    create_payment_request, get_payment_requests, accept_payment_request
)
from services.qr_service import generate_payment_qr, generate_wallet_qr
from core.security import get_current_user
from models import User
from config import settings

router = APIRouter()


# ============ PAYMENT LINKS ============

@router.post("/link/create", response_model=PaymentLinkResponse, summary="Create payment link")
def create_link(
    link_data: PaymentLinkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a payment link (like PayTM links).
    
    WHAT IT DOES:
    1. Creates a unique payment link
    2. Returns link that can be shared
    3. Others can pay via this link
    """
    payment_link = create_payment_link(
        db,
        current_user.id,
        link_data.amount,
        link_data.description,
        link_data.expires_hours
    )
    
    # Create response with payment URL
    base_url = "http://127.0.0.1:8000"  # You can make this configurable
    response = PaymentLinkResponse(
        id=payment_link.id,
        link_id=payment_link.link_id,
        amount=payment_link.amount,
        description=payment_link.description,
        is_active=bool(payment_link.is_active),
        expires_at=payment_link.expires_at,
        created_at=payment_link.created_at,
        payment_url=f"{base_url}/api/v1/payments/link/{payment_link.link_id}"
    )
    
    return response


@router.get("/link/{link_id}", response_model=PaymentLinkResponse, summary="Get payment link details")
def get_link_details(
    link_id: str,
    db: Session = Depends(get_db)
):
    """
    Get payment link details (public endpoint - no auth needed).
    """
    payment_link = get_payment_link(db, link_id)
    
    base_url = "http://127.0.0.1:8000"
    return PaymentLinkResponse(
        id=payment_link.id,
        link_id=payment_link.link_id,
        amount=payment_link.amount,
        description=payment_link.description,
        is_active=bool(payment_link.is_active),
        expires_at=payment_link.expires_at,
        created_at=payment_link.created_at,
        payment_url=f"{base_url}/api/v1/payments/link/{payment_link.link_id}"
    )


@router.post("/link/{link_id}/pay", response_model=TransactionResponse, summary="Pay via payment link")
def pay_link(
    link_id: str,
    request: PayLinkRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Pay via a payment link.
    
    WHAT IT DOES:
    1. Takes payment link ID
    2. Deducts money from your wallet
    3. Adds to link creator's wallet
    4. Marks link as used
    """
    return pay_via_link(db, link_id, request.wallet_id, current_user.id)


@router.get("/link/{link_id}/qr", response_model=QRCodeResponse, summary="Get QR code for payment link")
def get_link_qr(
    link_id: str,
    db: Session = Depends(get_db)
):
    """
    Get QR code for payment link.
    """
    payment_link = get_payment_link(db, link_id)
    qr_code = generate_payment_qr(link_id)
    
    return QRCodeResponse(
        qr_code=qr_code,
        data=f"pay/{link_id}"
    )


# ============ PAYMENT REQUESTS ============

@router.post("/request", response_model=PaymentRequestResponse, summary="Request money from someone")
def request_money(
    request_data: PaymentRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Request money from another user.
    
    WHAT IT DOES:
    1. Creates a payment request
    2. Recipient gets notified
    3. Recipient can accept/reject
    """
    payment_request = create_payment_request(
        db,
        current_user.id,
        request_data.recipient_email,
        request_data.amount,
        request_data.description
    )
    
    return PaymentRequestResponse(
        id=payment_request.id,
        requester_id=payment_request.requester_id,
        recipient_id=payment_request.recipient_id,
        amount=payment_request.amount,
        description=payment_request.description,
        status=payment_request.status,
        created_at=payment_request.created_at
    )


@router.get("/request/received", response_model=List[PaymentRequestResponse], summary="Get received payment requests")
def get_received_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get payment requests you received (people requesting money from you).
    """
    requests = get_payment_requests(db, current_user.id, "received")
    
    return [
        PaymentRequestResponse(
            id=req.id,
            requester_id=req.requester_id,
            recipient_id=req.recipient_id,
            amount=req.amount,
            description=req.description,
            status=req.status,
            created_at=req.created_at
        )
        for req in requests
    ]


@router.get("/request/sent", response_model=List[PaymentRequestResponse], summary="Get sent payment requests")
def get_sent_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get payment requests you sent to others.
    """
    requests = get_payment_requests(db, current_user.id, "sent")
    
    return [
        PaymentRequestResponse(
            id=req.id,
            requester_id=req.requester_id,
            recipient_id=req.recipient_id,
            amount=req.amount,
            description=req.description,
            status=req.status,
            created_at=req.created_at
        )
        for req in requests
    ]


@router.post("/request/{request_id}/accept", response_model=TransactionResponse, summary="Accept and pay a payment request")
def accept_request(
    request_id: int,
    request_data: AcceptPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Accept and pay a payment request.
    
    WHAT IT DOES:
    1. Takes payment request ID
    2. Deducts money from your wallet
    3. Adds to requester's wallet
    4. Marks request as completed
    """
    return accept_payment_request(db, request_id, request_data.wallet_id, current_user.id)


# ============ QR CODES ============

@router.get("/wallet/{wallet_id}/qr", response_model=QRCodeResponse, summary="Get QR code for wallet")
def get_wallet_qr(
    wallet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get QR code for your wallet (for receiving money).
    """
    from services.wallet_service import get_wallet
    
    # Verify wallet belongs to user
    wallet = get_wallet(db, wallet_id, current_user.id)
    
    qr_code = generate_wallet_qr(wallet_id)
    
    return QRCodeResponse(
        qr_code=qr_code,
        data=f"wallet/{wallet_id}"
    )
