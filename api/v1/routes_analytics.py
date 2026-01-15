"""
Analytics API routes.

WHAT THIS FILE DOES:
- Transaction statistics
- Spending analytics
- Daily summaries
- Reports

LEARN:
- Analytics = analyzing data
- Helps users understand spending patterns
- Helps merchants see revenue trends
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from core.security import get_current_user
from models import User
from schemas import (
    TransactionStatsResponse,
    DailySummaryResponse,
    SpendingBreakdownResponse
)
from services.analytics_service import (
    get_user_transaction_stats,
    get_daily_transaction_summary,
    get_spending_by_category
)

router = APIRouter()


@router.get("/stats", response_model=TransactionStatsResponse, summary="Get transaction statistics")
def get_transaction_stats(
    wallet_id: Optional[int] = Query(None, description="Filter by wallet ID"),
    days: int = Query(30, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get transaction statistics for your account.
    
    WHAT IT DOES:
    1. Gets all transactions in last N days
    2. Calculates totals by type (deposits, transfers, etc.)
    3. Returns statistics
    
    EXAMPLE OUTPUT:
    {
        "period_days": 30,
        "total_deposits": 1000.0,
        "total_transfers": 300.0,
        "transaction_count": 15,
        "average_transaction": 86.67
    }
    """
    return get_user_transaction_stats(db, current_user.id, wallet_id, days)


@router.get("/daily", response_model=DailySummaryResponse, summary="Get daily transaction summary")
def get_daily_summary(
    wallet_id: Optional[int] = Query(None, description="Filter by wallet ID"),
    date: Optional[str] = Query(None, description="Date (YYYY-MM-DD), defaults to today"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get daily transaction summary.
    
    WHAT IT DOES:
    1. Gets all transactions for a specific day
    2. Returns summary with transaction list
    
    EXAMPLE:
    GET /api/v1/analytics/daily?date=2026-01-13
    Returns all transactions for January 13, 2026
    """
    from datetime import datetime
    
    parsed_date = None
    if date:
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    return get_daily_transaction_summary(db, current_user.id, wallet_id, parsed_date)


@router.get("/breakdown", response_model=SpendingBreakdownResponse, summary="Get spending breakdown")
def get_breakdown(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get spending breakdown by category.
    
    WHAT IT DOES:
    1. Groups transactions by type
    2. Calculates totals for each type
    3. Returns breakdown
    
    EXAMPLE OUTPUT:
    {
        "deposits": 1000.0,
        "withdrawals": 200.0,
        "transfers": 300.0,
        "payments": 500.0
    }
    """
    return get_spending_by_category(db, current_user.id, days)
