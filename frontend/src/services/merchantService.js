/**
 * Merchant Service
 * 
 * WHAT THIS FILE DOES:
 * - Handles merchant account API calls
 */

import api from '../config/api';

/**
 * Register as merchant
 */
export const registerMerchant = async (businessName, businessType = null) => {
  const response = await api.post('/merchant/register', {
    business_name: businessName,
    business_type: businessType,
  });
  return response.data;
};

/**
 * Get merchant account
 */
export const getMerchant = async () => {
  const response = await api.get('/merchant/me');
  return response.data;
};

/**
 * Get merchant statistics
 */
export const getMerchantStats = async () => {
  const response = await api.get('/merchant/stats');
  return response.data;
};
