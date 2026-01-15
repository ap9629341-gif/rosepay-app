"""
Database models (tables).
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base


class TransactionType(str, enum.Enum):
    """Types of transactions."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"


class TransactionStatus(str, enum.Enum):
    """Status of a transaction."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class User(Base):
    """User model - stores user accounts."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    wallets = relationship("Wallet", back_populates="owner", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user")


class Wallet(Base):
    """Wallet model - stores user wallets."""
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    wallet_pin = Column(String, nullable=True)  # Encrypted PIN for security
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", foreign_keys="Transaction.wallet_id", back_populates="wallet", overlaps="recipient_wallet")


class Transaction(Base):
    """Transaction model - stores all payment history."""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    description = Column(String, nullable=True)
    recipient_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    wallet = relationship("Wallet", foreign_keys=[wallet_id], back_populates="transactions")
    recipient_wallet = relationship("Wallet", foreign_keys=[recipient_wallet_id])


class PaymentLink(Base):
    """Payment link model - like PayTM payment links."""
    __tablename__ = "payment_links"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    link_id = Column(String, unique=True, index=True, nullable=False)  # Unique payment link ID
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = used/expired
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)  # If paid
    
    # Relationships
    user = relationship("User")
    transaction = relationship("Transaction")


class PaymentRequest(Base):
    """Payment request model - request money from someone."""
    __tablename__ = "payment_requests"

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who requested
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who should pay
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    
    # Relationships
    requester = relationship("User", foreign_keys=[requester_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
    transaction = relationship("Transaction")


class Merchant(Base):
    """Merchant model - for businesses/vendors."""
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)  # One merchant per user
    business_name = Column(String, nullable=False)
    business_type = Column(String, nullable=True)  # e.g., "Restaurant", "Retail", etc.
    merchant_id = Column(String, unique=True, index=True, nullable=False)  # Unique merchant ID
    is_active = Column(Integer, default=1)
    total_revenue = Column(Float, default=0.0)  # Total money received
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")


class RecurringPayment(Base):
    """Recurring payment model - for subscriptions and automatic payments."""
    __tablename__ = "recurring_payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    recipient_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)  # For transfers
    recipient_email = Column(String, nullable=True)  # For payment requests
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    frequency = Column(String, nullable=False)  # "daily", "weekly", "monthly", "yearly"
    next_payment_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)  # Optional end date
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_paid_at = Column(DateTime, nullable=True)
    total_payments = Column(Integer, default=0)  # Count of payments made
    
    # Relationships
    user = relationship("User")
    wallet = relationship("Wallet", foreign_keys=[wallet_id])
    recipient_wallet = relationship("Wallet", foreign_keys=[recipient_wallet_id])


class BillSplit(Base):
    """Bill split model - for splitting expenses with friends."""
    __tablename__ = "bill_splits"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    total_amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    settled_at = Column(DateTime, nullable=True)
    
    # Relationships
    creator = relationship("User", foreign_keys=[creator_id])
    participants = relationship("BillSplitParticipant", back_populates="bill_split")


class BillSplitParticipant(Base):
    """Bill split participant model - tracks who owes what."""
    __tablename__ = "bill_split_participants"

    id = Column(Integer, primary_key=True, index=True)
    bill_split_id = Column(Integer, ForeignKey("bill_splits.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount_owed = Column(Float, nullable=False)  # How much this person owes
    amount_paid = Column(Float, default=0.0)  # How much they've paid
    is_settled = Column(Integer, default=0)  # 0 = not paid, 1 = paid
    settled_at = Column(DateTime, nullable=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    
    # Relationships
    bill_split = relationship("BillSplit", back_populates="participants")
    user = relationship("User")
    transaction = relationship("Transaction")


class Budget(Base):
    """Budget model - for tracking spending limits."""
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)  # null = all wallets
    category = Column(String, nullable=True)  # e.g., "Food", "Transport", "Entertainment"
    amount = Column(Float, nullable=False)  # Budget limit
    period = Column(String, nullable=False)  # "daily", "weekly", "monthly"
    current_spent = Column(Float, default=0.0)  # Amount spent in current period
    period_start = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    wallet = relationship("Wallet")
