/**
 * Transaction Service
 * 
 * WHAT THIS FILE DOES:
 * - Handles transaction history API calls
 * - Get transactions, filter by wallet, etc.
 */

import api from '../config/api';

/**
 * Get transaction history
 */
export const getTransactions = async (walletId = null, limit = 50) => {
  const url = walletId 
    ? `/transactions?wallet_id=${walletId}&limit=${limit}`
    : `/transactions?limit=${limit}`;
  
  const response = await api.get(url);
  return response.data;
};
