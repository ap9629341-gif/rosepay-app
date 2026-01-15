"""
Application configuration and settings.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./wallet_app.db"
    
    # Security - JWT token settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production-use-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App info
    APP_NAME: str = "RosePay - Wallet Payment API"
    APP_VERSION: str = "1.0.0"
    
    # Payment Gateway - Razorpay
    RAZORPAY_KEY_ID: str = "rzp_test_S3EO5kK0GT1iZS"  # Get from Razorpay dashboard
    RAZORPAY_KEY_SECRET: str = "2e7iELlEzuxVUo06Kay8U11b"  # Get from Razorpay dashboard
    
    # Email Settings (for notifications)
    SMTP_HOST: str = "smtp.gmail.com"  # Gmail SMTP server
    SMTP_PORT: int = 587  # Gmail port
    SMTP_USER: str = ""  # Your email (leave empty for now)
    SMTP_PASSWORD: str = ""  # Your email password (leave empty for now)
    EMAIL_FROM: str = "noreply@rosepay.com"  # Sender email
    
    # Transaction Limits
    MAX_TRANSACTION_AMOUNT: float = 10000.0  # Maximum single transaction
    MIN_TRANSACTION_AMOUNT: float = 0.01  # Minimum single transaction
    DAILY_TRANSACTION_LIMIT: float = 50000.0  # Maximum per day
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings object
settings = Settings()
