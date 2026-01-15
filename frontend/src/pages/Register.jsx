/**
 * Register Page Component
 * 
 * WHAT THIS COMPONENT DOES:
 * - Displays registration form
 * - Creates new user account
 * - Redirects to login after registration
 */

import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useFormValidation } from '../hooks/useFormValidation';
import { register } from '../services/authService';

function Register() {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const validationRules = {
    email: [
      (v) => !v && 'Email is required',
      (v) => !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) && 'Invalid email format',
    ],
    password: [
      (v) => !v && 'Password is required',
      (v) => v.length < 6 && 'Password must be at least 6 characters',
    ],
    confirmPassword: [
      (v, all) => !v && 'Please confirm your password',
      (v, all) => v !== all.password && 'Passwords do not match',
    ],
  };

  const {
    values: formData,
    errors,
    touched,
    handleChange,
    handleBlur,
    validateAll,
  } = useFormValidation(
    {
      email: '',
      password: '',
      confirmPassword: '',
      fullName: '',
    },
    validationRules
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!validateAll()) {
      toast.error('Please fix the errors in the form');
      return;
    }

    setLoading(true);

    try {
      await register(formData.email, formData.password, formData.fullName);
      toast.success('Registration successful! Please login.');
      navigate('/login');
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Registration failed. Please try again.';
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-rose-50 to-pink-100 dark:from-gray-900 dark:to-gray-800">
      <div className="card w-full max-w-md dark:bg-gray-800">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-rose-600 mb-2">RosePay</h1>
          <p className="text-gray-600">Create your account to get started.</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-1">
              Full Name
            </label>
            <input
              id="fullName"
              name="fullName"
              type="text"
              value={formData.fullName}
              onChange={handleChange}
              className="input-field"
              placeholder="John Doe"
            />
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              onBlur={handleBlur}
              className={`input-field ${touched.email && errors.email ? 'border-red-500' : ''}`}
              placeholder="you@example.com"
              required
            />
            {touched.email && errors.email && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.email}</p>
            )}
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              onBlur={handleBlur}
              className={`input-field ${touched.password && errors.password ? 'border-red-500' : ''}`}
              placeholder="••••••••"
              required
              minLength={6}
            />
            {touched.password && errors.password && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.password}</p>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              onBlur={handleBlur}
              className={`input-field ${touched.confirmPassword && errors.confirmPassword ? 'border-red-500' : ''}`}
              placeholder="••••••••"
              required
            />
            {touched.confirmPassword && errors.confirmPassword && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.confirmPassword}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                <span>Creating account...</span>
              </>
            ) : (
              'Register'
            )}
          </button>
        </form>

        <p className="mt-6 text-center text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="text-rose-600 font-semibold hover:underline">
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
