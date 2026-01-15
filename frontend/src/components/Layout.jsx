/**
 * Layout Component
 * 
 * WHAT THIS COMPONENT DOES:
 * - Wraps all pages with navigation bar
 * - Provides consistent layout
 * - Handles logout
 */

import { Link, useNavigate, useLocation } from 'react-router-dom';
import { logout, getCurrentUser } from '../services/authService';
import { useTheme } from '../contexts/ThemeContext';
import { useEffect, useState } from 'react';

function Layout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(getCurrentUser());
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => {
    return location.pathname === path ? 'text-rose-600 border-b-2 border-rose-600' : 'text-gray-600 hover:text-rose-600';
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      {/* Navigation Bar */}
      <nav className="bg-white dark:bg-gray-800 shadow-md transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <Link to="/dashboard" className="flex items-center">
                <span className="text-2xl font-bold text-rose-600 dark:text-rose-400">RosePay</span>
              </Link>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link
                  to="/dashboard"
                  className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${isActive('/dashboard')}`}
                >
                  Dashboard
                </Link>
                <Link
                  to="/transactions"
                  className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${isActive('/transactions')}`}
                >
                  Transactions
                </Link>
                <Link
                  to="/transfer"
                  className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${isActive('/transfer')}`}
                >
                  Transfer
                </Link>
                <Link
                  to="/payment-links"
                  className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${isActive('/payment-links')}`}
                >
                  Payment Links
                </Link>
                <Link
                  to="/analytics"
                  className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${isActive('/analytics')}`}
                >
                  Analytics
                </Link>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {user && (
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  {user.full_name || user.email}
                </span>
              )}
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
              >
                {theme === 'light' ? '🌙' : '☀️'}
              </button>
              <button
                onClick={handleLogout}
                className="btn-secondary text-sm"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}

export default Layout;
