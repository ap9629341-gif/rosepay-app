/**
 * Main App Component
 * 
 * WHAT THIS FILE DOES:
 * - Sets up React Router
 * - Defines all routes
 * - Wraps protected routes with authentication
 * 
 * LEARN:
 * - Router = Handles navigation between pages
 * - Routes = URL paths that show different components
 * - Protected routes = Require authentication
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { ThemeProvider } from './contexts/ThemeContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Transfer from './pages/Transfer';
import PaymentLinks from './pages/PaymentLinks';
import Analytics from './pages/Analytics';

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 3000,
            style: {
              background: 'var(--toast-bg)',
              color: 'var(--toast-color)',
            },
            success: {
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/transactions"
          element={
            <ProtectedRoute>
              <Layout>
                <Transactions />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/transfer"
          element={
            <ProtectedRoute>
              <Layout>
                <Transfer />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/payment-links"
          element={
            <ProtectedRoute>
              <Layout>
                <PaymentLinks />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/analytics"
          element={
            <ProtectedRoute>
              <Layout>
                <Analytics />
              </Layout>
            </ProtectedRoute>
          }
        />
        
        {/* Default redirect */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
