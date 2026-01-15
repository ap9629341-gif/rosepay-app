/**
 * Dashboard Page Component
 * 
 * WHAT THIS COMPONENT DOES:
 * - Shows wallet balance
 * - Displays recent transactions
 * - Quick actions (add money, transfer)
 */

import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import LoadingSpinner from '../components/LoadingSpinner';
import { getWallets } from '../services/walletService';
import { getTransactions } from '../services/transactionService';

function Dashboard() {
  const [wallets, setWallets] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [walletsData, transactionsData] = await Promise.all([
        getWallets(),
        getTransactions(null, 5), // Get last 5 transactions
      ]);
      setWallets(walletsData);
      setTransactions(transactionsData);
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const totalBalance = wallets.reduce((sum, wallet) => sum + wallet.balance, 0);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" text="Loading dashboard..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-600">Welcome back! Here's your account overview.</p>
      </div>

      {/* Total Balance Card */}
      <div className="card bg-gradient-to-r from-rose-600 to-pink-600 text-white">
        <div className="flex justify-between items-center">
          <div>
            <p className="text-rose-100 text-sm font-medium">Total Balance</p>
            <p className="text-4xl font-bold mt-2">${totalBalance.toFixed(2)}</p>
          </div>
          <div className="text-6xl opacity-20">💰</div>
        </div>
      </div>

      {/* Wallets Grid */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Your Wallets</h2>
          <Link to="/transfer" className="btn-primary text-sm">
            Create Wallet
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {wallets.length === 0 ? (
            <div className="col-span-full card text-center py-8">
              <p className="text-gray-600 mb-4">No wallets yet. Create your first wallet!</p>
              <Link to="/transfer" className="btn-primary">
                Create Wallet
              </Link>
            </div>
          ) : (
            wallets.map((wallet) => (
              <div key={wallet.id} className="card">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-sm text-gray-600">Wallet #{wallet.id}</p>
                    <p className="text-2xl font-bold text-gray-900 mt-1">
                      ${wallet.balance.toFixed(2)}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">{wallet.currency}</p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Link
                    to={`/transfer?wallet=${wallet.id}`}
                    className="flex-1 btn-secondary text-center text-sm py-2"
                  >
                    Transfer
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Recent Transactions */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Recent Transactions</h2>
          <Link to="/transactions" className="text-rose-600 hover:underline text-sm">
            View All
          </Link>
        </div>
        <div className="card">
          {transactions.length === 0 ? (
            <p className="text-gray-600 text-center py-8">No transactions yet.</p>
          ) : (
            <div className="space-y-4">
              {transactions.map((transaction) => (
                <div
                  key={transaction.id}
                  className="flex justify-between items-center py-3 border-b border-gray-200 last:border-0"
                >
                  <div>
                    <p className="font-medium text-gray-900">
                      {transaction.transaction_type.charAt(0).toUpperCase() + 
                       transaction.transaction_type.slice(1)}
                    </p>
                    <p className="text-sm text-gray-600">
                      {transaction.description || 'No description'}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(transaction.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <p
                      className={`font-semibold ${
                        transaction.transaction_type === 'deposit' ||
                        transaction.transaction_type === 'payment'
                          ? 'text-green-600'
                          : 'text-red-600'
                      }`}
                    >
                      {transaction.transaction_type === 'deposit' ||
                      transaction.transaction_type === 'payment'
                        ? '+'
                        : '-'}
                      ${transaction.amount.toFixed(2)}
                    </p>
                    <p
                      className={`text-xs mt-1 px-2 py-1 rounded-full inline-block ${
                        transaction.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : transaction.status === 'pending'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {transaction.status}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
