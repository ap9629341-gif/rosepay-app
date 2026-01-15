"""
Recurring Payment API routes.

WHAT THIS FILE DOES:
- Handles recurring payment creation
- Lists recurring payments
- Cancels recurring payments
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from core.security import get_current_user
from models import User
from schemas import RecurringPaymentCreate, RecurringPaymentResponse
from services.recurring_payment_service import (
    create_recurring_payment,
    get_user_recurring_payments,
    cancel_recurring_payment
)

router = APIRouter()


@router.post("/create", response_model=RecurringPaymentResponse, summary="Create recurring payment")
def create_recurring(
    request: RecurringPaymentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a recurring payment (subscription, automatic transfer).
    
    WHAT IT DOES:
    1. Creates recurring payment schedule
    2. Sets next payment date
    3. Returns recurring payment details
    
    EXAMPLE:
    - Monthly subscription: $10/month
    - Weekly transfer: $50/week to friend
    - Daily payment: $5/day for service
    """
    return create_recurring_payment(db, current_user.id, request)


@router.get("/list", response_model=list[RecurringPaymentResponse], summary="Get my recurring payments")
def list_recurring(
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all your recurring payments.
    
    WHAT IT DOES:
    1. Gets all recurring payments for current user
    2. Shows active and/or inactive
    3. Returns list of recurring payments
    """
    return get_user_recurring_payments(db, current_user.id, active_only)


@router.post("/{recurring_id}/cancel", response_model=RecurringPaymentResponse, summary="Cancel recurring payment")
def cancel_recurring(
    recurring_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a recurring payment.
    
    WHAT IT DOES:
    1. Deactivates recurring payment
    2. Stops future payments
    3. Returns updated recurring payment
    """
    return cancel_recurring_payment(db, recurring_id, current_user.id)
