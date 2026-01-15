/**
 * Protected Route Component
 * 
 * WHAT THIS COMPONENT DOES:
 * - Protects routes that require authentication
 * - Redirects to login if user is not authenticated
 * 
 * LEARN:
 * - Higher Order Component pattern
 * - Route protection = Security for pages
 */

import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../services/authService';

function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;
