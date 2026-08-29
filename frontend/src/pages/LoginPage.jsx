import React, { useState } from 'react';
import { Shield, Lock, Mail, UserCheck, Key, ShieldAlert } from 'lucide-react';

export default function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('analyst_jane');
  const [password, setPassword] = useState('••••••••••••');
  const [role, setRole] = useState('Security Analyst');

  const roles = [
    { id: 'Security Analyst', title: 'Security Analyst', desc: 'File uploads, static scans, reports' },
    { id: 'SOC Team Member', title: 'SOC Team Member', desc: 'Monitor logs, active threats & alerts' },
    { id: 'Administrator', title: 'Administrator', desc: 'User management & security policies' },
    { id: 'Researcher', title: 'Researcher', desc: 'Malware datasets & threat analytics' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    onLoginSuccess({
      username: username || 'analyst_jane',
      email: `${username}@threatlens.ai`,
      role: role
    });
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Cyber Glow Grid */}
      <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:24px_24px] opacity-30"></div>
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl"></div>
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-cyan-600/10 rounded-full blur-3xl"></div>

      <div className="w-full max-w-md bg-[#111827] border border-gray-800 rounded-2xl p-8 shadow-2xl relative z-10 cyber-glow-blue">
        {/* Header Branding */}
        <div className="text-center mb-8">
          <div className="inline-flex p-3 bg-blue-600/10 border border-blue-500/30 rounded-2xl mb-3 text-blue-400">
            <Shield className="w-10 h-10" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            ThreatLens AI
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Malware Classification & Threat Detection System
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Username Input */}
          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
              Username / Operator ID
            </label>
            <div className="relative">
              <Mail className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full bg-gray-900/90 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                placeholder="analyst_jane"
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

          {/* Role Selection Dropdown */}
          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
              System Access Role
            </label>
            <div className="relative">
              <UserCheck className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full bg-gray-900/90 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all appearance-none"
              >
                {roles.map((r) => (
                  <option key={r.id} value={r.id} className="bg-gray-900 text-white">
                    {r.title}
                  </option>
                ))}
              </select>
            </div>
            <p className="text-[11px] text-gray-400 mt-1">
              Role controls access permissions across ThreatLens AI platform.
            </p>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold py-3 px-4 rounded-xl shadow-lg hover:shadow-blue-500/20 transition-all flex items-center justify-center space-x-2"
          >
            <Key className="w-4 h-4" />
            <span>Authenticate & Access Dashboard</span>
          </button>
        </form>

        <div className="mt-6 pt-4 border-t border-gray-800/80 text-center">
          <span className="text-xs text-gray-400 flex items-center justify-center">
            <ShieldAlert className="w-3.5 h-3.5 mr-1 text-emerald-400" />
            Protected SOC Environment • Milestone 1 Ready
          </span>
        </div>
      </div>
    </div>
  );
}
