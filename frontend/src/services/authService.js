/**
 * Authentication Service
 * 
 * WHAT THIS FILE DOES:
 * - Handles user login and registration
 * - Stores authentication token
 * - Provides functions to check if user is logged in
 * 
 * LEARN:
 * - Service = Functions that handle specific tasks
 * - Token = JWT token for authentication
 * - localStorage = Browser storage (persists after page refresh)
 */

import api from '../config/api';

/**
 * Register a new user
 * 
 * WHAT IT DOES:
 * 1. Sends user data to backend
 * 2. Backend creates user account
 * 3. Returns user data
 */
export const register = async (email, password, fullName) => {
  const response = await api.post('/users/register', {
    email,
    password,
    full_name: fullName,
  });
  return response.data;
};

/**
 * Login user
 * 
 * WHAT IT DOES:
 * 1. Sends email and password to backend
 * 2. Backend validates credentials
 * 3. Returns access token
 * 4. Stores token in localStorage
 */
export const login = async (email, password) => {
  const response = await api.post('/users/login', {
    email: email,
    password: password,
  });
  
  // Store token and user data
  const { access_token, user } = response.data;
  localStorage.setItem('token', access_token);
  if (user) {
    localStorage.setItem('user', JSON.stringify(user));
  }
  
  return { access_token, user };
};

/**
 * Logout user
 * 
 * WHAT IT DOES:
 * 1. Removes token from localStorage
 * 2. Removes user data
 */
export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

/**
 * Get current user from localStorage
 */
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};
