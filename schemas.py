"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

from models import TransactionType, TransactionStatus


# ============ USER SCHEMAS ============

class UserBase(BaseModel):
    """Base user data."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str


# ============ WALLET SCHEMAS ============

class WalletBase(BaseModel):
    """Base wallet data."""
    currency: str = "USD"


class WalletCreate(WalletBase):
    """Schema for creating a wallet."""
    pass


class WalletResponse(WalletBase):
    """Schema for wallet response."""
    id: int
    user_id: int
    balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class AddMoneyRequest(BaseModel):
    """Schema for adding money to wallet."""
    amount: float
    description: Optional[str] = None


class SetWalletPINRequest(BaseModel):
    """Schema for setting wallet PIN."""
    pin: str


class VerifyPINRequest(BaseModel):
    """Schema for verifying wallet PIN."""
    pin: str


# ============ TRANSACTION SCHEMAS ============

class TransactionBase(BaseModel):
    """Base transaction data."""
    amount: float
    transaction_type: TransactionType
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    wallet_id: int
    recipient_wallet_id: Optional[int] = None


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: int
    user_id: int
    wallet_id: int
    status: TransactionStatus
    recipient_wallet_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransferRequest(BaseModel):
    """Schema for transferring money."""
    recipient_wallet_id: int
    amount: float
    description: Optional[str] = None


class TransferWithPINRequest(TransferRequest):
    """Schema for transferring money with PIN verification."""
    pin: str


# ============ PAYMENT LINK SCHEMAS ============

class PaymentLinkCreate(BaseModel):
    """Schema for creating a payment link."""
    amount: float
    description: Optional[str] = None
    expires_hours: Optional[int] = 24  # Link expires in X hours


class PaymentLinkResponse(BaseModel):
    """Schema for payment link response."""
    id: int
    link_id: str
    amount: float
    description: Optional[str] = None
    is_active: bool
    expires_at: Optional[datetime] = None
    created_at: datetime
    payment_url: str  # Full URL to pay
    
    class Config:
        from_attributes = True


class PayLinkRequest(BaseModel):
    """Schema for paying via link."""
    wallet_id: int


# ============ PAYMENT REQUEST SCHEMAS ============

class PaymentRequestCreate(BaseModel):
    """Schema for creating a payment request."""
    recipient_email: EmailStr
    amount: float
    description: Optional[str] = None


class PaymentRequestResponse(BaseModel):
    """Schema for payment request response."""
    id: int
    requester_id: int
    recipient_id: int
    amount: float
    description: Optional[str] = None
    status: TransactionStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


class AcceptPaymentRequest(BaseModel):
    """Schema for accepting a payment request."""
    wallet_id: int


# ============ QR CODE SCHEMAS ============

class QRCodeResponse(BaseModel):
    """Schema for QR code response."""
    qr_code: str  # Base64 encoded image
    data: str  # What the QR code contains


# ============ PAYMENT GATEWAY SCHEMAS ============

class CreateGatewayOrderRequest(BaseModel):
    """Schema for creating a payment gateway order."""
    amount: float
    currency: str = "INR"
    description: Optional[str] = None


class GatewayOrderResponse(BaseModel):
    """Schema for payment gateway order response."""
    order_id: str
    amount: float
    currency: str
    key_id: str  # Razorpay key ID for frontend
    receipt: str


class VerifyPaymentRequest(BaseModel):
    """Schema for verifying payment after gateway callback."""
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    wallet_id: int
    amount: float
    description: Optional[str] = None


class PaymentStatusResponse(BaseModel):
    """Schema for payment status response."""
    payment_id: str
    status: str
    amount: float
    currency: str
    method: str


# ============ MERCHANT SCHEMAS ============

class MerchantCreate(BaseModel):
    """Schema for creating a merchant account."""
    business_name: str
    business_type: Optional[str] = None


class MerchantResponse(BaseModel):
    """Schema for merchant response."""
    id: int
    user_id: int
    business_name: str
    business_type: Optional[str]
    merchant_id: str
    is_active: bool
    total_revenue: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class MerchantStatsResponse(BaseModel):
    """Schema for merchant statistics."""
    merchant_id: str
    business_name: str
    business_type: Optional[str]
    total_revenue: float
    transaction_count: int
    is_active: bool


# ============ ANALYTICS SCHEMAS ============

class TransactionStatsResponse(BaseModel):
    """Schema for transaction statistics."""
    period_days: int
    total_deposits: float
    total_withdrawals: float
    total_transfers: float
    total_payments: float
    transaction_count: int
    average_transaction: float


class DailySummaryResponse(BaseModel):
    """Schema for daily transaction summary."""
    date: str
    transaction_count: int
    total_amount: float
    transactions: List[dict]


class SpendingBreakdownResponse(BaseModel):
    """Schema for spending breakdown by category."""
    deposits: float
    withdrawals: float
    transfers: float
    payments: float


# ============ RECURRING PAYMENT SCHEMAS ============

class RecurringPaymentCreate(BaseModel):
    """Schema for creating a recurring payment."""
    wallet_id: int
    recipient_wallet_id: Optional[int] = None
    recipient_email: Optional[EmailStr] = None
    amount: float
    description: Optional[str] = None
    frequency: str  # "daily", "weekly", "monthly", "yearly"
    end_date: Optional[datetime] = None


class RecurringPaymentResponse(BaseModel):
    """Schema for recurring payment response."""
    id: int
    user_id: int
    wallet_id: int
    recipient_wallet_id: Optional[int]
    amount: float
    description: Optional[str]
    frequency: str
    next_payment_date: datetime
    end_date: Optional[datetime]
    is_active: bool
    total_payments: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ BILL SPLIT SCHEMAS ============

class BillSplitCreate(BaseModel):
    """Schema for creating a bill split."""
    title: str
    description: Optional[str] = None
    total_amount: float
    currency: str = "USD"
    participants: List[dict]  # [{"user_id": 1, "amount": 25.0}, ...]


class BillSplitResponse(BaseModel):
    """Schema for bill split response."""
    id: int
    creator_id: int
    title: str
    description: Optional[str]
    total_amount: float
    currency: str
    status: TransactionStatus
    created_at: datetime
    participants: List[dict]
    
    class Config:
        from_attributes = True


# ============ BUDGET SCHEMAS ============

class BudgetCreate(BaseModel):
    """Schema for creating a budget."""
    wallet_id: Optional[int] = None  # null = all wallets
    category: Optional[str] = None
    amount: float
    period: str  # "daily", "weekly", "monthly"


class BudgetResponse(BaseModel):
    """Schema for budget response."""
    id: int
    user_id: int
    wallet_id: Optional[int]
    category: Optional[str]
    amount: float
    period: str
    current_spent: float
    remaining: float
    percentage_used: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
