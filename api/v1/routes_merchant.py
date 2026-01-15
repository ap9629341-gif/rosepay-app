"""
Merchant API routes.

WHAT THIS FILE DOES:
- Handles merchant account creation
- Merchant statistics
- Merchant management

LEARN:
- Routes = API endpoints (URLs)
- Each function handles one endpoint
- Uses FastAPI decorators (@router.post, etc.)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from core.security import get_current_user
from models import User
from schemas import MerchantCreate, MerchantResponse, MerchantStatsResponse
from services.merchant_service import (
    create_merchant,
    get_user_merchant,
    get_merchant_stats
)

router = APIRouter()


@router.post("/register", response_model=MerchantResponse, summary="Register as merchant")
def register_merchant(
    request: MerchantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Register as a merchant (business/vendor).
    
    WHAT IT DOES:
    1. Creates merchant account for current user
    2. Generates unique merchant ID
    3. Returns merchant details
    
    EXAMPLE:
    User registers as "Pizza Shop" → Gets merchant ID "MRCH_ABC123"
    Now they can accept payments as a business!
    """
    return create_merchant(db, current_user.id, request.business_name, request.business_type)


@router.get("/me", response_model=MerchantResponse, summary="Get my merchant account")
def get_my_merchant(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get your merchant account details.
    
    WHAT IT DOES:
    1. Gets merchant account for current user
    2. Returns merchant details
    """
    return get_user_merchant(db, current_user.id)


@router.get("/stats", response_model=MerchantStatsResponse, summary="Get merchant statistics")
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get merchant statistics and revenue.
    
    WHAT IT DOES:
    1. Gets merchant account
    2. Calculates statistics (revenue, transaction count)
    3. Returns stats
    
    EXAMPLE OUTPUT:
    {
        "merchant_id": "MRCH_ABC123",
        "business_name": "Pizza Shop",
        "total_revenue": 5000.0,
        "transaction_count": 150
    }
    """
    return get_merchant_stats(db, current_user.id)
