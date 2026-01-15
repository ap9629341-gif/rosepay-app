/**
 * Wallet Service
 * 
 * WHAT THIS FILE DOES:
 * - Handles all wallet-related API calls
 * - Create wallet, get balance, add money, transfer
 * 
 * LEARN:
 * - Service pattern = Separates API calls from components
 * - Makes code reusable and easier to maintain
 */

import api from '../config/api';

/**
 * Get all wallets for current user
 */
export const getWallets = async () => {
  const response = await api.get('/wallets');
  return response.data;
};

/**
 * Get specific wallet by ID
 */
export const getWallet = async (walletId) => {
  const response = await api.get(`/wallets/${walletId}`);
  return response.data;
};

/**
 * Create a new wallet
 */
export const createWallet = async (currency = 'USD') => {
  const response = await api.post('/wallets', { currency });
  return response.data;
};

/**
 * Add money to wallet
 */
export const addMoney = async (walletId, amount, description) => {
  const response = await api.post(`/wallets/${walletId}/add-money`, {
    amount,
    description,
  });
  return response.data;
};

/**
 * Transfer money to another wallet
 */
export const transferMoney = async (walletId, recipientWalletId, amount, description) => {
  const response = await api.post(`/wallets/${walletId}/transfer`, {
    recipient_wallet_id: recipientWalletId,
    amount,
    description,
  });
  return response.data;
};

/**
 * Set wallet PIN
 */
export const setWalletPIN = async (walletId, pin) => {
  const response = await api.post(`/wallets/${walletId}/set-pin`, {
    pin,
  });
  return response.data;
};
