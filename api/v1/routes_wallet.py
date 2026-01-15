"""
Wallet routes - wallet management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import (
    WalletCreate, WalletResponse, AddMoneyRequest, TransferRequest, 
    TransactionResponse, SetWalletPINRequest, VerifyPINRequest, TransferWithPINRequest
)
from services.wallet_service import (
    create_wallet,
    get_user_wallets,
    get_wallet,
    add_money_to_wallet,
    transfer_money,
    get_wallet_balance
)
from core.security import get_current_user
from models import User

router = APIRouter()


@router.post("/", response_model=WalletResponse, summary="Create new wallet")
def create_new_wallet(
    wallet: WalletCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new wallet for the current user.
    
    WHAT IT DOES:
    1. Creates a wallet with balance 0
    2. Links it to the logged-in user
    3. Returns wallet info
    """
    return create_wallet(db, current_user.id, wallet.currency)


@router.get("/", response_model=List[WalletResponse], summary="Get all user wallets")
def list_wallets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all wallets for the current user.
    """
    return get_user_wallets(db, current_user.id)


@router.get("/{wallet_id}", response_model=WalletResponse, summary="Get wallet details")
def get_wallet_details(
    wallet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific wallet.
    """
    return get_wallet(db, wallet_id, current_user.id)


@router.get("/{wallet_id}/balance", summary="Get wallet balance")
def get_balance(
    wallet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the balance of a wallet.
    """
    balance = get_wallet_balance(db, wallet_id, current_user.id)
    return {"wallet_id": wallet_id, "balance": balance}


@router.post("/{wallet_id}/add-money", response_model=TransactionResponse, summary="Add money to wallet")
def add_money(
    wallet_id: int,
    request: AddMoneyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add money to a wallet (deposit).
    
    WHAT IT DOES:
    1. Increases wallet balance
    2. Creates a transaction record
    3. Returns transaction details
    """
    return add_money_to_wallet(db, wallet_id, current_user.id, request)


@router.post("/{wallet_id}/transfer", response_model=TransactionResponse, summary="Transfer money")
def transfer(
    wallet_id: int,
    request: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transfer money from your wallet to another wallet.
    
    WHAT IT DOES:
    1. Validates transaction limits
    2. Deducts money from your wallet
    3. Adds money to recipient wallet
    4. Creates transaction record
    5. Sends email notifications
    6. Returns transaction details
    """
    return transfer_money(db, wallet_id, current_user.id, request)


@router.post("/{wallet_id}/set-pin", response_model=WalletResponse, summary="Set wallet PIN")
def set_pin(
    wallet_id: int,
    request: SetWalletPINRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set or update wallet PIN for security.
    
    WHAT IT DOES:
    1. Validates PIN (4-6 digits)
    2. Encrypts PIN
    3. Saves to wallet
    4. Returns updated wallet
    
    SECURITY:
    - PIN is encrypted before storing
    - Required for transfers/withdrawals
    """
    from services.wallet_pin_service import set_wallet_pin
    return set_wallet_pin(db, wallet_id, current_user.id, request.pin)


@router.post("/{wallet_id}/verify-pin", summary="Verify wallet PIN")
def verify_pin(
    wallet_id: int,
    request: VerifyPINRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify wallet PIN.
    
    WHAT IT DOES:
    1. Checks if PIN is correct
    2. Returns success/failure
    """
    from services.wallet_pin_service import verify_wallet_pin
    is_valid = verify_wallet_pin(db, wallet_id, current_user.id, request.pin)
    return {"valid": is_valid}
