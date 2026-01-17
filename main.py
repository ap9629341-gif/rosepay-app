from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from api.v1 import (
    routes_wallet, routes_transactions, routes_users, routes_health, 
    routes_payments, routes_gateway, routes_merchant, routes_analytics,
    routes_recurring, routes_billsplit, routes_budget
)
from database import init_db
from core.error_handlers import (
    validation_exception_handler,
    integrity_error_handler,
    general_exception_handler
)

app = FastAPI(title="RosePay - Wallet Payment API", version="1.0.0")

# Add CORS middleware (allows frontend to make API calls)
import os

# Get CORS origins from environment or use defaults
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,https://frontend-livid-eight-59.vercel.app")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Supports multiple origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register error handlers (NEW FEATURE!)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register routers
app.include_router(routes_wallet.router, prefix="/api/v1/wallets", tags=["wallets"])
app.include_router(
    routes_transactions.router, prefix="/api/v1/transactions", tags=["transactions"]
)
app.include_router(routes_users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(routes_payments.router, prefix="/api/v1/payments", tags=["payments"])
app.include_router(routes_gateway.router, prefix="/api/v1/gateway", tags=["payment-gateway"])
app.include_router(routes_merchant.router, prefix="/api/v1/merchant", tags=["merchant"])
app.include_router(routes_analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(routes_recurring.router, prefix="/api/v1/recurring", tags=["recurring-payments"])
app.include_router(routes_billsplit.router, prefix="/api/v1/billsplit", tags=["bill-split"])
app.include_router(routes_budget.router, prefix="/api/v1/budget", tags=["budget"])
app.include_router(routes_health.router, prefix="/api/v1", tags=["health"])


@app.get("/")
def read_root():
    return {
        "message": "RosePay - Wallet Payment API is running",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.on_event("startup")
async def startup_event():
    """Initialize database when app starts."""
    try:
        init_db()
        print("✅ Database initialized!")
        print("✅ RosePay API is ready!")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
        print("✅ API is ready (database will initialize on first use)")

