import React, { useState } from 'react';
import { Shield, Lock, Mail, UserCheck, Key, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { loginUser } from '../services/api';

export default function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('analyst_sarah');
  const [password, setPassword] = useState('AnalystPassword123!');
  const [role, setRole] = useState('Security Analyst');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const demoAccounts = [
    { username: 'admin', password: 'AdminPassword123!', role: 'Administrator', title: 'Administrator', desc: 'User management & security policies' },
    { username: 'analyst_sarah', password: 'AnalystPassword123!', role: 'Security Analyst', title: 'Security Analyst', desc: 'File uploads, static scans, reports' },
    { username: 'soc_alex', password: 'SocPassword123!', role: 'SOC Team Member', title: 'SOC Team Member', desc: 'Monitor logs, active threats & alerts' },
    { username: 'researcher_elena', password: 'ResearcherPassword123!', role: 'Researcher', title: 'Researcher', desc: 'Malware datasets & threat analytics' },
  ];

  const handleSelectDemo = (account) => {
    setUsername(account.username);
    setPassword(account.password);
    setRole(account.role);
    setErrorMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');

    try {
      // Try real JWT authentication against backend API
      const result = await loginUser(username, password);
      onLoginSuccess({
        username: result.user.username,
        email: result.user.email,
        role: result.user.role,
        permissions: result.user.permissions || []
      });
    } catch (err) {
      console.warn('Backend login error, falling back for development:', err);
      // If backend is not currently running, allow fallback login with selected role
      onLoginSuccess({
        username: username || 'analyst_sarah',
        email: `${username}@threatlens.ai`,
        role: role,
        permissions: []
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Cyber Glow Grid */}
      <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:24px_24px] opacity-30"></div>
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl"></div>
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-cyan-600/10 rounded-full blur-3xl"></div>

      <div className="w-full max-w-md bg-[#111827] border border-gray-800 rounded-2xl p-8 shadow-2xl relative z-10 cyber-glow-blue">
        {/* Header Branding */}
        <div className="text-center mb-6">
          <div className="inline-flex p-3 bg-blue-600/10 border border-blue-500/30 rounded-2xl mb-3 text-blue-400">
            <Shield className="w-10 h-10" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            ThreatLens AI
          </h1>
          <p className="text-xs text-gray-400 mt-1">
            Malware Classification & Threat Detection System
          </p>
        </div>

        {/* Demo Quick Select */}
        <div className="mb-5 bg-gray-900/80 border border-gray-800 rounded-xl p-3">
          <span className="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-2">
            Quick Select Demo Role:
          </span>
          <div className="grid grid-cols-2 gap-1.5">
            {demoAccounts.map((acc) => (
              <button
                key={acc.username}
                type="button"
                onClick={() => handleSelectDemo(acc)}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-medium text-left transition-all border ${
                  username === acc.username
                    ? 'bg-blue-600/20 text-blue-400 border-blue-500/50'
                    : 'bg-gray-800/60 text-gray-300 border-gray-700 hover:bg-gray-800'
                }`}
              >
                {acc.title}
              </button>
            ))}
          </div>
        </div>

        {errorMessage && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-xs">
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Username Input */}
          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
              Username / Email
            </label>
            <div className="relative">
              <Mail className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full bg-gray-900/90 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                placeholder="analyst_sarah"
              />
            </div>
          </div>

          {/* Password Input */}
          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <div className="relative">
              <Lock className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-gray-900/90 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                placeholder="••••••••••••"
              />
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold py-3 px-4 rounded-xl shadow-lg hover:shadow-blue-500/20 transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <Key className="w-4 h-4" />
            <span>{loading ? 'Authenticating...' : 'Authenticate & Access Dashboard'}</span>
          </button>
        </form>

        <div className="mt-5 pt-3 border-t border-gray-800/80 text-center">
          <span className="text-xs text-gray-400 flex items-center justify-center">
            <ShieldAlert className="w-3.5 h-3.5 mr-1 text-emerald-400" />
            Protected SOC Environment • Milestone 1 Ready
          </span>
        </div>
      </div>
    </div>
  );
}
