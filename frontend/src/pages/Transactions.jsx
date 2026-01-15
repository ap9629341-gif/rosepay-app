/**
 * Transactions Page Component
 * 
 * WHAT THIS COMPONENT DOES:
 * - Shows full transaction history
 * - Filter by wallet
 * - Search transactions
 */

import { useEffect, useState } from 'react';
import { getTransactions } from '../services/transactionService';
import { getWallets } from '../services/walletService';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [wallets, setWallets] = useState([]);
  const [selectedWallet, setSelectedWallet] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWallets();
  }, []);

  useEffect(() => {
    loadTransactions();
  }, [selectedWallet]);

  const loadWallets = async () => {
    try {
      const data = await getWallets();
      setWallets(data);
    } catch (error) {
      console.error('Error loading wallets:', error);
    }
  };

  const loadTransactions = async () => {
    setLoading(true);
    try {
      const data = await getTransactions(
        selectedWallet || null,
        100
      );
      setTransactions(data);
    } catch (error) {
      console.error('Error loading transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'deposit':
      case 'payment':
        return 'text-green-600';
      case 'withdrawal':
      case 'transfer':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Transaction History</h1>
        <p className="mt-1 text-sm text-gray-600">View all your transactions</p>
      </div>

      {/* Filter */}
      <div className="card">
        <label htmlFor="wallet" className="block text-sm font-medium text-gray-700 mb-2">
          Filter by Wallet
        </label>
        <select
          id="wallet"
          value={selectedWallet}
          onChange={(e) => setSelectedWallet(e.target.value)}
          className="input-field"
        >
          <option value="">All Wallets</option>
          {wallets.map((wallet) => (
            <option key={wallet.id} value={wallet.id}>
              Wallet #{wallet.id} - ${wallet.balance.toFixed(2)}
            </option>
          ))}
        </select>
      </div>

      {/* Transactions List */}
      <div className="card">
        {loading ? (
          <div className="text-center py-8 text-gray-600">Loading...</div>
        ) : transactions.length === 0 ? (
          <div className="text-center py-8 text-gray-600">No transactions found.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {transactions.map((transaction) => (
                  <tr key={transaction.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(transaction.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {transaction.transaction_type.charAt(0).toUpperCase() +
                       transaction.transaction_type.slice(1)}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {transaction.description || 'No description'}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm font-semibold ${getTypeColor(transaction.transaction_type)}`}>
                      {(transaction.transaction_type === 'deposit' ||
                        transaction.transaction_type === 'payment'
                        ? '+'
                        : '-') + '$' + transaction.amount.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(transaction.status)}`}
                      >
                        {transaction.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Transactions;
