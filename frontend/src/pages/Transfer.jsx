/**
 * Transfer Page Component
 * 
 * WHAT THIS COMPONENT DOES:
 * - Transfer money between wallets
 * - Add money to wallet
 * - Create new wallet
 */

import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import LoadingSpinner from '../components/LoadingSpinner';
import ConfirmDialog from '../components/ConfirmDialog';
import { getWallets, transferMoney, addMoney, createWallet } from '../services/walletService';
import { useNavigate } from 'react-router-dom';

function Transfer() {
  const [wallets, setWallets] = useState([]);
  const [formData, setFormData] = useState({
    type: 'transfer', // 'transfer' or 'add'
    senderWalletId: '',
    recipientWalletId: '',
    amount: '',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showConfirm, setShowConfirm] = useState(false);
  const [pendingAction, setPendingAction] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadWallets();
  }, []);

  const loadWallets = async () => {
    try {
      const data = await getWallets();
      setWallets(data);
      if (data.length > 0) {
        setFormData((prev) => ({ ...prev, senderWalletId: data[0].id.toString() }));
      }
    } catch (error) {
      console.error('Error loading wallets:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
    setSuccess('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    // Show confirmation for transfers
    if (formData.type === 'transfer') {
      setPendingAction(() => () => executeTransaction());
      setShowConfirm(true);
      return;
    }
    
    // Execute immediately for add money
    executeTransaction();
  };

  const executeTransaction = async () => {
    setLoading(true);

    try {
      if (formData.type === 'add') {
        await addMoney(
          parseInt(formData.senderWalletId),
          parseFloat(formData.amount),
          formData.description
        );
        const msg = `Successfully added $${formData.amount} to wallet!`;
        setSuccess(msg);
        toast.success(msg);
      } else {
        await transferMoney(
          parseInt(formData.senderWalletId),
          parseInt(formData.recipientWalletId),
          parseFloat(formData.amount),
          formData.description
        );
        const msg = `Successfully transferred $${formData.amount}!`;
        setSuccess(msg);
        toast.success(msg);
      }
      
      // Reset form
      setFormData({
        type: formData.type,
        senderWalletId: formData.senderWalletId,
        recipientWalletId: '',
        amount: '',
        description: '',
      });
      
      // Reload wallets to get updated balances
      await loadWallets();
      
      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Transaction failed. Please try again.';
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWallet = async () => {
    try {
      await createWallet('USD');
      await loadWallets();
      const msg = 'Wallet created successfully!';
      setSuccess(msg);
      toast.success(msg);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to create wallet.';
      setError(errorMsg);
      toast.error(errorMsg);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Transfer Money</h1>
        <p className="mt-1 text-sm text-gray-600">Send money or add funds to your wallet</p>
      </div>

      {error && (
        <div className="card bg-red-50 border border-red-200">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {success && (
        <div className="card bg-green-50 border border-green-200">
          <p className="text-green-800">{success}</p>
        </div>
      )}

      <ConfirmDialog
        isOpen={showConfirm}
        onClose={() => setShowConfirm(false)}
        onConfirm={() => pendingAction && pendingAction()}
        title="Confirm Transfer"
        message={`Are you sure you want to transfer $${formData.amount} to wallet #${formData.recipientWalletId}?`}
        confirmText="Transfer"
        cancelText="Cancel"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex space-x-4 mb-6">
              <button
                type="button"
                onClick={() => {
                  setFormData({ ...formData, type: 'transfer' });
                  setError('');
                  setSuccess('');
                }}
                className={`flex-1 py-2 rounded-lg font-semibold transition-colors ${
                  formData.type === 'transfer'
                    ? 'bg-rose-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Transfer Money
              </button>
              <button
                type="button"
                onClick={() => {
                  setFormData({ ...formData, type: 'add' });
                  setError('');
                  setSuccess('');
                }}
                className={`flex-1 py-2 rounded-lg font-semibold transition-colors ${
                  formData.type === 'add'
                    ? 'bg-rose-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Add Money
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="senderWalletId" className="block text-sm font-medium text-gray-700 mb-1">
                  {formData.type === 'add' ? 'Wallet' : 'From Wallet'}
                </label>
                <select
                  id="senderWalletId"
                  name="senderWalletId"
                  value={formData.senderWalletId}
                  onChange={handleChange}
                  className="input-field"
                  required
                >
                  <option value="">Select wallet</option>
                  {wallets.map((wallet) => (
                    <option key={wallet.id} value={wallet.id}>
                      Wallet #{wallet.id} - ${wallet.balance.toFixed(2)}
                    </option>
                  ))}
                </select>
              </div>

              {formData.type === 'transfer' && (
                <div>
                  <label htmlFor="recipientWalletId" className="block text-sm font-medium text-gray-700 mb-1">
                    To Wallet ID
                  </label>
                  <input
                    id="recipientWalletId"
                    name="recipientWalletId"
                    type="number"
                    value={formData.recipientWalletId}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="Enter recipient wallet ID"
                    required={formData.type === 'transfer'}
                  />
                </div>
              )}

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
                  Description (Optional)
                </label>
                <input
                  id="description"
                  name="description"
                  type="text"
                  value={formData.description}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="What is this for?"
                />
              </div>

              <button
                type="submit"
                disabled={loading || wallets.length === 0}
                className="btn-primary w-full py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {loading ? (
                  <>
                    <LoadingSpinner size="sm" text="" />
                    <span className="ml-2">Processing...</span>
                  </>
                ) : formData.type === 'add' ? (
                  'Add Money'
                ) : (
                  'Transfer Money'
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">Your Wallets</h3>
            {wallets.length === 0 ? (
              <div>
                <p className="text-sm text-gray-600 mb-4">No wallets yet.</p>
                <button onClick={handleCreateWallet} className="btn-primary w-full text-sm">
                  Create Wallet
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                {wallets.map((wallet) => (
                  <div key={wallet.id} className="p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm font-medium text-gray-900">Wallet #{wallet.id}</p>
                    <p className="text-2xl font-bold text-gray-900">
                      ${wallet.balance.toFixed(2)}
                    </p>
                    <p className="text-xs text-gray-500">{wallet.currency}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Transfer;
