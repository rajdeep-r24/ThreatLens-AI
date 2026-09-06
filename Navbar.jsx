import React from 'react';
import {
  Shield,
  LayoutDashboard,
  UploadCloud,
  FileText,
  LogOut,
  Bell
} from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  currentUser,
  onLogout
}) {
  return (
    <nav className="bg-[#111827] border-b border-gray-800 sticky top-0 z-50">

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        <div className="flex items-center justify-between h-16">

          {/* Brand */}
          <div
            className="flex items-center space-x-3 cursor-pointer"
            onClick={() => setActiveTab('dashboard')}
          >
            <div className="p-2 bg-blue-600/20 border border-blue-500/40 rounded-lg text-blue-400">
              <Shield className="w-6 h-6" />
            </div>

            <div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                ThreatLens AI
              </span>

              <span className="block text-[10px] text-gray-400 uppercase tracking-widest font-mono">
                Malware Detection & Analytics
              </span>
            </div>
          </div>

          {/* Navigation */}
          <div className="hidden md:flex items-center space-x-1">

            {/* Dashboard */}
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
              }`}
            >
              <LayoutDashboard className="w-4 h-4 mr-2" />
              Dashboard
            </button>

            {/* Upload */}
            <button
              onClick={() => setActiveTab('upload')}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'upload'
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
              }`}
            >
              <UploadCloud className="w-4 h-4 mr-2" />
              Upload & Scan
            </button>

            {/* Analysis */}
            <button
              onClick={() => setActiveTab('results')}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'results'
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
              }`}
            >
              <FileText className="w-4 h-4 mr-2" />
              Analysis Reports
            </button>

            {/* Member 5 Alerts */}
            <button
              onClick={() => setActiveTab('alerts')}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'alerts'
                  ? 'bg-red-600/20 text-red-400 border border-red-500/30'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
              }`}
            >
              <Bell className="w-4 h-4 mr-2" />
              Alerts & Reports
            </button>

          </div>

          {/* User */}
          <div className="flex items-center space-x-3">

            <div className="hidden lg:flex items-center text-xs space-x-2 px-3 py-1.5 bg-gray-800/80 rounded-full border border-gray-700">

              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>

              <span className="text-gray-300 font-medium">
                {currentUser?.username || 'Analyst'}
              </span>

              <span className="text-blue-400 bg-blue-950/80 px-2 py-0.5 rounded border border-blue-800/60 text-[10px] font-semibold">
                {currentUser?.role || 'Security Analyst'}
              </span>

            </div>

            <button
              onClick={onLogout}
              title="Logout"
              className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-950/40 rounded-lg transition-colors border border-transparent hover:border-red-900/40"
            >
              <LogOut className="w-5 h-5" />
            </button>

          </div>

        </div>

      </div>

    </nav>
  );
}