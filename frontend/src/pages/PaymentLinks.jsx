/**
 * Payment Links Page Component
 * 
 * WHAT THIS COMPONENT DOES:
 * - Create payment links
 * - View created links
 * - Pay payment links
 */

import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { createPaymentLink, getPaymentLinkQR } from '../services/paymentService';

function PaymentLinks() {
  const [formData, setFormData] = useState({
    amount: '',
    description: '',
    expiresInHours: 24,
  });
  const [createdLink, setCreatedLink] = useState(null);
  const [qrCode, setQrCode] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setCreatedLink(null);
    setQrCode(null);

    try {
      const link = await createPaymentLink(
        parseFloat(formData.amount),
        formData.description,
        parseInt(formData.expiresInHours)
      );
      setCreatedLink(link);

      // Get QR code
      try {
        const qr = await getPaymentLinkQR(link.link_id);
        setQrCode(qr.qr_code_data);
      } catch (qrError) {
        console.error('Error loading QR code:', qrError);
      }
      toast.success('Payment link created successfully!');
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to create payment link.';
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Link copied to clipboard!');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Payment Links</h1>
        <p className="mt-1 text-sm text-gray-600">Create shareable payment links</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Create Link Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Create Payment Link</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-1">
                Amount ($)
              </label>
              <input
                id="amount"
                name="amount"
                type="number"
                step="0.01"
                min="0.01"
                value={formData.amount}
                onChange={handleChange}
                className="input-field"
                placeholder="0.00"
                required
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <input
                id="description"
                name="description"
                type="text"
                value={formData.description}
                onChange={handleChange}
                className="input-field"
                placeholder="What is this payment for?"
              />
            </div>

            <div>
              <label htmlFor="expiresInHours" className="block text-sm font-medium text-gray-700 mb-1">
                Expires In (Hours)
              </label>
              <input
                id="expiresInHours"
                name="expiresInHours"
                type="number"
                min="1"
                value={formData.expiresInHours}
                onChange={handleChange}
                className="input-field"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating...' : 'Create Payment Link'}
            </button>
          </form>
        </div>

        {/* Created Link Display */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Payment Link</h2>

          {createdLink ? (
            <div className="space-y-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Link ID</p>
                <p className="font-mono text-sm font-semibold">{createdLink.link_id}</p>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Amount</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${createdLink.amount.toFixed(2)}
                </p>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Payment URL</p>
                <div className="flex items-center space-x-2">
                  <p className="font-mono text-xs text-gray-900 flex-1 break-all">
                    {createdLink.payment_url}
                  </p>
                  <button
                    onClick={() => copyToClipboard(createdLink.payment_url)}
                    className="btn-secondary text-xs px-3 py-1"
                  >
                    Copy
                  </button>
                </div>
              </div>

              {qrCode && (
                <div className="p-4 bg-gray-50 rounded-lg text-center">
                  <p className="text-sm text-gray-600 mb-2">QR Code</p>
                  <div
                    dangerouslySetInnerHTML={{ __html: qrCode }}
                    className="flex justify-center"
                  />
                </div>
              )}

              <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  Share this link or QR code with the payer. They can pay using their wallet.
                </p>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <p>Create a payment link to see it here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default PaymentLinks;
