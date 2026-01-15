/**
 * API Configuration
 * 
 * WHAT THIS FILE DOES:
 * - Sets up the base URL for API calls
 * - Creates axios instance with default config
 * - Handles authentication tokens
 * 
 * LEARN:
 * - Axios = HTTP client for making API requests
 * - Base URL = Common part of all API endpoints
 * - Interceptors = Code that runs before/after requests
 */

import axios from 'axios';

// Base URL for your FastAPI backend
// Use environment variable in production, localhost in development
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : 'http://127.0.0.1:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - adds token to every request
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('token');
    if (token) {
      // Add token to Authorization header
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handles errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If 401 (Unauthorized), clear token and redirect to login
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
