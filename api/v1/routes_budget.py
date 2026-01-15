"""
Budget API routes.

WHAT THIS FILE DOES:
- Handles budget management
- Creates budgets
- Tracks spending
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from core.security import get_current_user
from models import User
from schemas import BudgetCreate, BudgetResponse
from services.budget_service import (
    create_budget,
    get_user_budgets
)

router = APIRouter()


@router.post("/create", response_model=BudgetResponse, summary="Create budget")
def create_budget_endpoint(
    request: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a spending budget.
    
    WHAT IT DOES:
    1. Creates budget with limit
    2. Sets period (daily/weekly/monthly)
    3. Tracks spending
    4. Returns budget details
    
    EXAMPLE:
    - Monthly food budget: $500
    - Weekly entertainment: $100
    - Daily transport: $20
    """
    budget = create_budget(db, current_user.id, request)
    
    # Calculate remaining and percentage
    remaining = budget.amount - budget.current_spent
    percentage = (budget.current_spent / budget.amount * 100) if budget.amount > 0 else 0
    
    return {
        **BudgetResponse.from_orm(budget).dict(),
        "remaining": remaining,
        "percentage_used": percentage
    }


@router.get("/list", response_model=list[BudgetResponse], summary="Get my budgets")
def list_budgets(
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all your budgets.
    
    WHAT IT DOES:
    1. Gets all budgets for user
    2. Calculates current spending
    3. Shows remaining amount
    4. Shows percentage used
    """
    budgets = get_user_budgets(db, current_user.id, active_only)
    
    # Add calculated fields
    result = []
    for budget in budgets:
        remaining = budget.amount - budget.current_spent
        percentage = (budget.current_spent / budget.amount * 100) if budget.amount > 0 else 0
        
        result.append({
            "id": budget.id,
            "user_id": budget.user_id,
            "wallet_id": budget.wallet_id,
            "category": budget.category,
            "amount": budget.amount,
            "period": budget.period,
            "current_spent": budget.current_spent,
            "remaining": remaining,
            "percentage_used": percentage,
            "is_active": bool(budget.is_active),
            "created_at": budget.created_at
        })
    
    return result
