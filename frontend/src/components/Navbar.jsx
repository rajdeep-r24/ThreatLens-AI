import React from 'react';
import { Shield, LayoutDashboard, UploadCloud, FileText, User, LogOut, Sun, Moon } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, currentUser, onLogout, theme, toggleTheme }) {
  return (
    <nav className="bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-gray-800 sticky top-0 z-50 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div className="flex items-center space-x-3 cursor-pointer group" onClick={() => setActiveTab('dashboard')}>
            <div className="p-2 bg-blue-50 dark:bg-blue-500/10 border border-blue-200 dark:border-blue-500/20 rounded-xl text-blue-600 dark:text-blue-400 group-hover:bg-blue-100 dark:group-hover:bg-blue-500/20 transition-all">
              <Shield className="w-5 h-5 text-blue-600 dark:text-blue-500" />
            </div>
            <div>
              <span className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
                ThreatLens
              </span>
              <span className="block text-[11px] text-slate-500 dark:text-gray-400 font-medium tracking-wide">
                AI Threat Intelligence
              </span>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${
                activeTab === 'dashboard'
                  ? 'bg-blue-50 text-blue-700 dark:bg-gray-800 dark:text-white'
                  : 'text-slate-600 hover:bg-slate-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800/50'
              }`}
            >
              <LayoutDashboard className="w-4 h-4 mr-2" />
              Security Dashboard
            </button>

            <button
              onClick={() => setActiveTab('upload')}
              className={`flex items-center px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${
                activeTab === 'upload'
                  ? 'bg-blue-50 text-blue-700 dark:bg-gray-800 dark:text-white'
                  : 'text-slate-600 hover:bg-slate-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800/50'
              }`}
            >
              <UploadCloud className="w-4 h-4 mr-2" />
              Upload & Deep Scan
            </button>

            <button
              onClick={() => setActiveTab('results')}
              className={`flex items-center px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${
                activeTab === 'results'
                  ? 'bg-blue-50 text-blue-700 dark:bg-gray-800 dark:text-white'
                  : 'text-slate-600 hover:bg-slate-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800/50'
              }`}
            >
              <FileText className="w-4 h-4 mr-2" />
              Threat Reports & AI Analysis
            </button>
          </div>

          {/* Right Side: Profile & Theme Toggle */}
          <div className="flex items-center space-x-4">
            
            <button
              onClick={toggleTheme}
              className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
              title="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            <div className="flex items-center space-x-3">
              <div className="hidden lg:flex items-center text-xs space-x-2 px-3 py-1.5 bg-slate-100 dark:bg-slate-800 rounded-full border border-slate-200 dark:border-slate-700">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span className="text-slate-700 dark:text-gray-300 font-semibold">{currentUser?.username || 'Analyst'}</span>
                <span className="text-[10px] text-slate-400">({currentUser?.role || 'SOC'})</span>
              </div>

              <button
                onClick={onLogout}
                title="Logout"
                className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 rounded-lg transition-colors border border-transparent"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
