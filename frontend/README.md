# RosePay Frontend

Modern React frontend for the RosePay payment application.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Layout.jsx    # Main layout with navigation
│   │   └── ProtectedRoute.jsx  # Route protection
│   ├── pages/            # Page components
│   │   ├── Login.jsx      # Login page
│   │   ├── Register.jsx  # Registration page
│   │   ├── Dashboard.jsx  # Main dashboard
│   │   ├── Transactions.jsx  # Transaction history
│   │   ├── Transfer.jsx   # Transfer/add money
│   │   ├── PaymentLinks.jsx  # Payment links
│   │   └── Analytics.jsx # Analytics page
│   ├── services/         # API service functions
│   │   ├── authService.js
│   │   ├── walletService.js
│   │   ├── transactionService.js
│   │   ├── paymentService.js
│   │   ├── analyticsService.js
│   │   └── merchantService.js
│   ├── config/
│   │   └── api.js        # API configuration
│   ├── App.jsx           # Main app component with routing
│   └── main.jsx          # Entry point
├── tailwind.config.js    # Tailwind CSS configuration
└── package.json
```

## 🎨 Features

- **Authentication**: Login and registration
- **Dashboard**: Overview of wallets and transactions
- **Transactions**: Full transaction history with filters
- **Transfer**: Send money and add funds
- **Payment Links**: Create shareable payment links
- **Analytics**: Spending statistics and breakdowns
- **Responsive Design**: Works on mobile and desktop

## 🔧 Technologies Used

- **React 19**: UI library
- **React Router**: Navigation
- **Axios**: HTTP client for API calls
- **Tailwind CSS**: Styling
- **Vite**: Build tool

## 📝 API Configuration

The frontend connects to the FastAPI backend at `http://127.0.0.1:8000/api/v1`.

To change the API URL, edit `src/config/api.js`:

```javascript
const API_BASE_URL = 'http://your-backend-url/api/v1';
```

## 🎯 Key Concepts Explained

### Components
- **Functional Components**: React components written as functions
- **Hooks**: `useState` for state, `useEffect` for side effects
- **Props**: Data passed from parent to child components

### Services
- **Service Pattern**: Separates API calls from UI components
- **Axios Interceptors**: Automatically add auth tokens to requests
- **Error Handling**: Centralized error handling

### Routing
- **Protected Routes**: Routes that require authentication
- **Navigation**: Programmatic navigation with `useNavigate`

### State Management
- **Local State**: `useState` for component-specific state
- **localStorage**: Persists auth token and user data

## 🚦 Running the App

1. **Start Backend** (in project root):
   ```bash
   python3 -m uvicorn main:app --reload
   ```

2. **Start Frontend** (in frontend directory):
   ```bash
   npm run dev
   ```

3. **Open Browser**: Navigate to `http://localhost:5173`

## 📦 Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## 🐛 Troubleshooting

### CORS Errors
If you see CORS errors, make sure your FastAPI backend has CORS middleware enabled.

### API Connection Issues
- Check that the backend is running on `http://127.0.0.1:8000`
- Verify the API URL in `src/config/api.js`

### Authentication Issues
- Clear localStorage: `localStorage.clear()` in browser console
- Check that token is being stored after login
