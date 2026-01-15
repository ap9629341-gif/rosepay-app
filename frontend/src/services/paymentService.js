/**
 * Payment Service
 * 
 * WHAT THIS FILE DOES:
 * - Handles payment links, QR codes, payment requests
 */

import api from '../config/api';

/**
 * Create a payment link
 */
export const createPaymentLink = async (amount, description, expiresInHours = 24) => {
  const response = await api.post('/payments/link/create', {
    amount,
    description,
    expires_in_hours: expiresInHours,
  });
  return response.data;
};

/**
 * Get payment link details
 */
export const getPaymentLink = async (linkId) => {
  const response = await api.get(`/payments/link/${linkId}`);
  return response.data;
};

/**
 * Pay a payment link
 */
export const payPaymentLink = async (linkId, walletId) => {
  const response = await api.post(`/payments/link/${linkId}/pay`, {
    wallet_id: walletId,
  });
  return response.data;
};

/**
 * Get QR code for payment link
 */
export const getPaymentLinkQR = async (linkId) => {
  const response = await api.get(`/payments/link/${linkId}/qr`);
  return response.data;
};

/**
 * Create payment request
 */
export const createPaymentRequest = async (recipientEmail, amount, description) => {
  const response = await api.post('/payments/request/create', {
    recipient_email: recipientEmail,
    amount,
    description,
  });
  return response.data;
};

/**
 * Get payment requests
 */
export const getPaymentRequests = async () => {
  const response = await api.get('/payments/requests');
  return response.data;
};

/**
 * Accept payment request
 */
export const acceptPaymentRequest = async (requestId, walletId) => {
  const response = await api.post(`/payments/request/${requestId}/accept`, {
    wallet_id: walletId,
  });
  return response.data;
};
