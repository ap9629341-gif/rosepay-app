# 🌹 RosePay - Wallet Payment API

A complete payment application like PayTM, Google Pay, and PhonePe built with FastAPI.

## ✨ Features

### Core Features
- ✅ User Registration & Authentication (JWT tokens)
- ✅ Wallet Management (Create, View, Balance)
- ✅ Add Money to Wallet
- ✅ Transfer Money between Wallets
- ✅ Transaction History

### Advanced Features (Like PayTM/Google Pay)
- ✅ **Payment Links** - Create shareable payment links
- ✅ **QR Code Generation** - Generate QR codes for payments
- ✅ **Payment Requests** - Request money from other users
- ✅ **Secure Transactions** - All transactions are logged and secure

## 🚀 Quick Start

### 1. Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 2. Run the Server

```bash
python3 -m uvicorn main:app --reload
```

### 3. Access the API

- **API Documentation**: http://127.0.0.1:8000/docs
- **Root Endpoint**: http://127.0.0.1:8000

## 📚 API Endpoints

### User Management
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - Login and get token

### Wallet Management
- `POST /api/v1/wallets` - Create wallet
- `GET /api/v1/wallets` - Get all your wallets
- `GET /api/v1/wallets/{wallet_id}` - Get wallet details
- `GET /api/v1/wallets/{wallet_id}/balance` - Get balance
- `POST /api/v1/wallets/{wallet_id}/add-money` - Add money
- `POST /api/v1/wallets/{wallet_id}/transfer` - Transfer money

### Payment Links (Like PayTM Links)
- `POST /api/v1/payments/link/create` - Create payment link
- `GET /api/v1/payments/link/{link_id}` - Get link details
- `POST /api/v1/payments/link/{link_id}/pay` - Pay via link
- `GET /api/v1/payments/link/{link_id}/qr` - Get QR code for link

### Payment Requests
- `POST /api/v1/payments/request` - Request money from someone
- `GET /api/v1/payments/request/received` - Get received requests
- `GET /api/v1/payments/request/sent` - Get sent requests
- `POST /api/v1/payments/request/{request_id}/accept` - Accept and pay request

### Transactions
- `GET /api/v1/transactions` - Get transaction history
- `GET /api/v1/transactions/{transaction_id}` - Get transaction details

## 🔐 Authentication

Most endpoints require authentication. After login, you'll get a JWT token. Use it like this:

1. Go to `/docs`
2. Click "Authorize" button (top right)
3. Enter: `Bearer YOUR_TOKEN_HERE`
4. Click "Authorize"

## 📖 Example Usage

### 1. Register a User
```json
POST /api/v1/users/register
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

### 2. Login
```json
POST /api/v1/users/login
{
  "email": "user@example.com",
  "password": "password123"
}
```
Returns: `{"access_token": "...", "token_type": "bearer"}`

### 3. Create Wallet
```json
POST /api/v1/wallets
{
  "currency": "USD"
}
```

### 4. Add Money
```json
POST /api/v1/wallets/{wallet_id}/add-money
{
  "amount": 100.0,
  "description": "Initial deposit"
}
```

### 5. Create Payment Link
```json
POST /api/v1/payments/link/create
{
  "amount": 50.0,
  "description": "Payment for services",
  "expires_hours": 24
}
```

### 6. Request Money
```json
POST /api/v1/payments/request
{
  "recipient_email": "friend@example.com",
  "amount": 25.0,
  "description": "Lunch money"
}
```

## 🗄️ Database

The app uses SQLite by default (stored in `wallet_app.db`). The database is automatically created when you first run the app.

## 🔧 Configuration

Edit `config.py` to change:
- Database URL
- JWT secret key
- Token expiration time
- App name and version

## 📦 Project Structure

```
payment_app/
├── main.py                 # FastAPI app entry point
├── database.py             # Database setup
├── models.py               # Database models
├── schemas.py              # Pydantic schemas
├── config.py               # Configuration
├── api/
│   └── v1/
│       ├── routes_users.py      # User endpoints
│       ├── routes_wallet.py     # Wallet endpoints
│       ├── routes_transactions.py  # Transaction endpoints
│       ├── routes_payments.py   # Payment links & requests
│       └── routes_health.py     # Health check
├── services/
│   ├── user_service.py          # User business logic
│   ├── wallet_service.py        # Wallet business logic
│   ├── transaction_service.py   # Transaction logic
│   ├── payment_link_service.py  # Payment link logic
│   ├── payment_request_service.py  # Payment request logic
│   └── qr_service.py            # QR code generation
└── core/
    └── security.py              # Security utilities
```

## 🚀 Next Steps

To make it production-ready like PayTM/Google Pay:

1. **Add Payment Gateway** (Razorpay, Stripe)
2. **Add Email Notifications**
3. **Add Mobile App** (React Native/Flutter)
4. **Add Web Frontend** (React/Vue)
5. **Add KYC Verification**
6. **Add Transaction Limits**
7. **Deploy to Cloud** (AWS, Heroku, etc.)

## 📝 License

This is a learning project. Feel free to use and modify!

## 🤝 Contributing

This is a beginner-friendly project. Feel free to add features and improve!

---

**Built with ❤️ using FastAPI**
