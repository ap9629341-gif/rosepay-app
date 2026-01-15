"""
Wallet service - handles wallet operations.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import Wallet, Transaction, TransactionType, TransactionStatus
from schemas import AddMoneyRequest, TransferRequest


def create_wallet(db: Session, user_id: int, currency: str = "USD") -> Wallet:
    """
    Create a new wallet for a user.
    
    WHAT IT DOES:
    1. Create a wallet with balance 0
    2. Link it to the user
    3. Return the wallet
    """
    wallet = Wallet(
        user_id=user_id,
        balance=0.0,
        currency=currency
    )
    
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    
    return wallet


def get_wallet(db: Session, wallet_id: int, user_id: int) -> Wallet:
    """
    Get a wallet (only if user owns it).
    
    SECURITY: Users can only access their own wallets!
    """
    wallet = db.query(Wallet).filter(
        Wallet.id == wallet_id,
        Wallet.user_id == user_id
    ).first()
    
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    
    return wallet


def get_user_wallets(db: Session, user_id: int) -> list[Wallet]:
    """Get all wallets for a user."""
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()


def add_money_to_wallet(
    db: Session,
    wallet_id: int,
    user_id: int,
    request: AddMoneyRequest
) -> Transaction:
    """
    Add money to a wallet (deposit).
    
    WHAT IT DOES:
    1. Validate transaction (amount limits, daily limits)
    2. Get the wallet
    3. Increase balance
    4. Create transaction record
    5. Send email notification
    6. Return transaction
    """
    # Validate transaction (NEW FEATURE!)
    from services.transaction_limits_service import validate_transaction
    validate_transaction(db, user_id, wallet_id, request.amount)
    
    wallet = get_wallet(db, wallet_id, user_id)
    
    # Update balance
    wallet.balance += request.amount
    
    # Create transaction record
    transaction = Transaction(
        user_id=user_id,
        wallet_id=wallet_id,
        amount=request.amount,
        transaction_type=TransactionType.DEPOSIT,
        status=TransactionStatus.COMPLETED,
        description=request.description or "Deposit"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    # Send email notification (NEW FEATURE!)
    try:
        from services.email_service import send_transaction_notification
        from models import User
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            send_transaction_notification(
                user_email=user.email,
                transaction_type="deposit",
                amount=request.amount,
                description=request.description or "Deposit",
                balance=wallet.balance
            )
    except Exception as e:
        # Don't fail transaction if email fails
        print(f"⚠️ Email notification failed: {str(e)}")
    
    return transaction


def transfer_money(
    db: Session,
    sender_wallet_id: int,
    user_id: int,
    request: TransferRequest
) -> Transaction:
    """
    Transfer money from one wallet to another.
    
    WHAT IT DOES:
    1. Get sender wallet (check ownership)
    2. Get recipient wallet
    3. Check if sender has enough balance
    4. Deduct from sender, add to recipient
    5. Create transaction records
    """
    # Get sender wallet
    sender_wallet = get_wallet(db, sender_wallet_id, user_id)
    
    # Validate transaction (NEW FEATURE!)
    from services.transaction_limits_service import validate_transaction
    validate_transaction(db, user_id, sender_wallet_id, request.amount)
    
    # Check balance
    if sender_wallet.balance < request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )
    
    # Get recipient wallet
    recipient_wallet = db.query(Wallet).filter(
        Wallet.id == request.recipient_wallet_id
    ).first()
    
    if not recipient_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient wallet not found"
        )
    
    # Update balances
    sender_wallet.balance -= request.amount
    recipient_wallet.balance += request.amount
    
    # Create transaction record
    transaction = Transaction(
        user_id=user_id,
        wallet_id=sender_wallet_id,
        amount=request.amount,
        transaction_type=TransactionType.TRANSFER,
        status=TransactionStatus.COMPLETED,
        description=request.description or "Transfer",
        recipient_wallet_id=request.recipient_wallet_id
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    # Send email notifications (NEW FEATURE!)
    try:
        from services.email_service import send_transaction_notification
        from models import User
        # Notify sender
        sender = db.query(User).filter(User.id == user_id).first()
        if sender:
            send_transaction_notification(
                user_email=sender.email,
                transaction_type="transfer",
                amount=request.amount,
                description=request.description or "Transfer",
                balance=sender_wallet.balance
            )
        # Notify recipient
        recipient = db.query(User).filter(User.id == recipient_wallet.user_id).first()
        if recipient:
            send_transaction_notification(
                user_email=recipient.email,
                transaction_type="deposit",
                amount=request.amount,
                description=f"Received: {request.description or 'Transfer'}",
                balance=recipient_wallet.balance
            )
    except Exception as e:
        print(f"⚠️ Email notification failed: {str(e)}")
    
    return transaction


def get_wallet_balance(db: Session, wallet_id: int, user_id: int) -> float:
    """Get wallet balance."""
    wallet = get_wallet(db, wallet_id, user_id)
    return wallet.balance
