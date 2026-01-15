/**
 * Analytics Page Component
 * 
 * WHAT THIS COMPONENT DOES:
 * - Shows transaction statistics
 * - Spending breakdown
 * - Visual charts (basic)
 */

import { useEffect, useState } from 'react';
import { getTransactionStats, getSpendingBreakdown } from '../services/analyticsService';
import { getWallets } from '../services/walletService';

function Analytics() {
  const [stats, setStats] = useState(null);
  const [breakdown, setBreakdown] = useState(null);
  const [wallets, setWallets] = useState([]);
  const [selectedWallet, setSelectedWallet] = useState('');
  const [days, setDays] = useState(30);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWallets();
  }, []);

  useEffect(() => {
    loadAnalytics();
  }, [selectedWallet, days]);

  const loadWallets = async () => {
    try {
      const data = await getWallets();
      setWallets(data);
    } catch (error) {
      console.error('Error loading wallets:', error);
    }
  };

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const [statsData, breakdownData] = await Promise.all([
        getTransactionStats(selectedWallet || null, days),
        getSpendingBreakdown(days),
      ]);
      setStats(statsData);
      setBreakdown(breakdownData);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <p className="mt-1 text-sm text-gray-600">View your spending patterns and statistics</p>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="wallet" className="block text-sm font-medium text-gray-700 mb-2">
              Wallet
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
                  Wallet #{wallet.id}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="days" className="block text-sm font-medium text-gray-700 mb-2">
              Period (Days)
            </label>
            <select
              id="days"
              value={days}
              onChange={(e) => setDays(parseInt(e.target.value))}
              className="input-field"
            >
              <option value={7}>Last 7 days</option>
              <option value={30}>Last 30 days</option>
              <option value={90}>Last 90 days</option>
            </select>
          </div>
        </div>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Total Deposits</p>
            <p className="text-2xl font-bold text-green-600">
              ${stats.total_deposits.toFixed(2)}
            </p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Total Transfers</p>
            <p className="text-2xl font-bold text-red-600">
              ${stats.total_transfers.toFixed(2)}
            </p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Transaction Count</p>
            <p className="text-2xl font-bold text-gray-900">{stats.transaction_count}</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Average Transaction</p>
            <p className="text-2xl font-bold text-gray-900">
              ${stats.average_transaction.toFixed(2)}
            </p>
          </div>
        </div>
      )}

      {/* Spending Breakdown */}
      {breakdown && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Spending Breakdown</h2>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Deposits</span>
                <span className="text-sm font-semibold text-green-600">
                  ${breakdown.deposits.toFixed(2)}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-600 h-2 rounded-full"
                  style={{
                    width: `${(breakdown.deposits / (breakdown.deposits + breakdown.withdrawals + breakdown.transfers + breakdown.payments)) * 100}%`,
                  }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Withdrawals</span>
                <span className="text-sm font-semibold text-red-600">
                  ${breakdown.withdrawals.toFixed(2)}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-red-600 h-2 rounded-full"
                  style={{
                    width: `${(breakdown.withdrawals / (breakdown.deposits + breakdown.withdrawals + breakdown.transfers + breakdown.payments)) * 100}%`,
                  }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Transfers</span>
                <span className="text-sm font-semibold text-orange-600">
                  ${breakdown.transfers.toFixed(2)}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-orange-600 h-2 rounded-full"
                  style={{
                    width: `${(breakdown.transfers / (breakdown.deposits + breakdown.withdrawals + breakdown.transfers + breakdown.payments)) * 100}%`,
                  }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Payments</span>
                <span className="text-sm font-semibold text-blue-600">
                  ${breakdown.payments.toFixed(2)}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full"
                  style={{
                    width: `${(breakdown.payments / (breakdown.deposits + breakdown.withdrawals + breakdown.transfers + breakdown.payments)) * 100}%`,
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Analytics;
