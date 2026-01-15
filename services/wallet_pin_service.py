"""
Wallet PIN security service.

WHAT THIS FILE DOES:
- Sets wallet PIN for security
- Verifies PIN before sensitive operations (transfers, withdrawals)
- Encrypts PIN (never store plain PIN!)

LEARN:
- PIN adds extra security layer
- Like ATM PIN - required for transactions
- PIN is hashed (encrypted) before storing
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import bcrypt

from models import Wallet


def set_wallet_pin(
    db: Session,
    wallet_id: int,
    user_id: int,
    pin: str
) -> Wallet:
    """
    Set or update wallet PIN.
    
    WHAT IT DOES:
    1. Validates PIN (must be 4-6 digits)
    2. Hashes PIN (encrypts it)
    3. Saves to database
    4. Returns wallet
    
    SECURITY:
    - PIN is hashed (encrypted) before storing
    - Never store plain PIN!
    - Like password hashing
    """
    from services.wallet_service import get_wallet
    
    wallet = get_wallet(db, wallet_id, user_id)
    
    # Validate PIN
    if not pin.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PIN must contain only digits"
        )
    
    if len(pin) < 4 or len(pin) > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PIN must be 4-6 digits"
        )
    
    # Hash PIN (encrypt it)
    pin_hash = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Save to wallet
    wallet.wallet_pin = pin_hash
    
    db.commit()
    db.refresh(wallet)
    
    return wallet


def verify_wallet_pin(
    db: Session,
    wallet_id: int,
    user_id: int,
    pin: str
) -> bool:
    """
    Verify wallet PIN.
    
    WHAT IT DOES:
    1. Gets wallet
    2. Compares provided PIN with stored hash
    3. Returns True if correct, False if wrong
    
    USAGE:
    Call this before allowing transfers/withdrawals
    """
    from services.wallet_service import get_wallet
    
    wallet = get_wallet(db, wallet_id, user_id)
    
    # Check if PIN is set
    if not wallet.wallet_pin:
        # No PIN set, allow transaction (for convenience)
        return True
    
    # Verify PIN
    try:
        return bcrypt.checkpw(pin.encode('utf-8'), wallet.wallet_pin.encode('utf-8'))
    except Exception:
        return False


def require_wallet_pin(
    db: Session,
    wallet_id: int,
    user_id: int,
    pin: str
) -> None:
    """
    Require wallet PIN for transaction.
    
    WHAT IT DOES:
    1. Verifies PIN
    2. Raises error if PIN is wrong or missing
    
    USAGE:
    Call this in transfer/withdrawal functions
    """
    if not verify_wallet_pin(db, wallet_id, user_id, pin):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid wallet PIN"
        )
