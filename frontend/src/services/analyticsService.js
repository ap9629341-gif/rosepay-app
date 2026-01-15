/**
 * Analytics Service
 * 
 * WHAT THIS FILE DOES:
 * - Handles analytics and statistics API calls
 */

import api from '../config/api';

/**
 * Get transaction statistics
 */
export const getTransactionStats = async (walletId = null, days = 30) => {
  const url = walletId
    ? `/analytics/stats?wallet_id=${walletId}&days=${days}`
    : `/analytics/stats?days=${days}`;
  
  const response = await api.get(url);
  return response.data;
};

/**
 * Get daily transaction summary
 */
export const getDailySummary = async (walletId = null, date = null) => {
  let url = '/analytics/daily';
  const params = new URLSearchParams();
  if (walletId) params.append('wallet_id', walletId);
  if (date) params.append('date', date);
  if (params.toString()) url += `?${params.toString()}`;
  
  const response = await api.get(url);
  return response.data;
};

/**
 * Get spending breakdown
 */
export const getSpendingBreakdown = async (days = 30) => {
  const response = await api.get(`/analytics/breakdown?days=${days}`);
  return response.data;
};
