import React, { useState } from 'react';
import {
  Shield,
  LayoutDashboard,
  UploadCloud,
  FileText,
  LogOut,
  Sun,
  Moon,
  Menu,
  X
} from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  currentUser,
  onLogout,
  theme,
  toggleTheme
}) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleNavigation = (tab) => {
    setActiveTab(tab);
    setMobileMenuOpen(false);
  };

  const navItems = [
    {
      id: 'dashboard',
      label: 'Security Dashboard',
      icon: LayoutDashboard
    },
    {
      id: 'upload',
      label: 'Upload & Deep Scan',
      icon: UploadCloud
    },
    {
      id: 'results',
      label: 'Threat Reports & AI Analysis',
      icon: FileText
    }
  ];

  return (
    <nav className="bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-gray-800 sticky top-0 z-50 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Main Navbar */}
        <div className="flex items-center justify-between min-h-16 py-2">

          {/* Brand Logo */}
          <div
            className="flex items-center space-x-3 cursor-pointer min-w-0"
            onClick={() => handleNavigation('dashboard')}
          >
            <div className="flex-shrink-0 p-2 bg-blue-50 dark:bg-blue-600/20 border border-blue-200 dark:border-blue-500/40 rounded-xl text-blue-600 dark:text-blue-400">
              <Shield className="w-5 h-5 sm:w-6 sm:h-6" />
            </div>

            <div className="min-w-0">
              <span className="block text-lg sm:text-xl font-bold text-slate-900 dark:text-white tracking-tight truncate">
                ThreatLens
              </span>

              <span className="hidden sm:block text-[11px] text-slate-500 dark:text-gray-400 font-medium tracking-wide truncate">
                AI Threat Intelligence
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => handleNavigation(id)}
                className={`flex items-center px-3 lg:px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
                  activeTab === id
                    ? 'bg-blue-50 text-blue-700 dark:bg-gray-800 dark:text-white'
                    : 'text-slate-600 hover:bg-slate-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800/50'
                }`}
              >
                <Icon className="w-4 h-4 mr-2 flex-shrink-0" />
                <span>{label}</span>
              </button>
            ))}
          </div>

          {/* Right Side: Theme, Profile & Logout */}
          <div className="flex items-center space-x-2 sm:space-x-3">

            {/* Theme Toggle */}
            {toggleTheme && (
              <button
                onClick={toggleTheme}
                className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                title="Toggle Theme"
                aria-label="Toggle Theme"
              >
                {theme === 'dark' ? <Sun className="w-4 h-4 sm:w-5 sm:h-5" /> : <Moon className="w-4 h-4 sm:w-5 sm:h-5" />}
              </button>
            )}

            {/* User Profile */}
            <div className="hidden lg:flex items-center text-xs space-x-2 px-3 py-1.5 bg-slate-100 dark:bg-gray-800/80 rounded-full border border-slate-200 dark:border-gray-700 max-w-xs">
              <span className="relative flex h-2 w-2 flex-shrink-0">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>

              <span className="text-slate-700 dark:text-gray-300 font-medium truncate">
                {currentUser?.username || 'Analyst'}
              </span>

              <span className="text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/80 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-800/60 text-[10px] font-semibold whitespace-nowrap">
                {currentUser?.role || 'Security Analyst'}
              </span>
            </div>

            {/* Logout */}
            <button
              onClick={onLogout}
              title="Logout"
              aria-label="Logout"
              className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 rounded-lg transition-colors border border-transparent flex-shrink-0"
            >
              <LogOut className="w-5 h-5" />
            </button>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen((prev) => !prev)}
              aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
              aria-expanded={mobileMenuOpen}
              className="md:hidden p-2 text-slate-600 dark:text-gray-400 hover:bg-slate-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              {mobileMenuOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </button>

          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-slate-200 dark:border-gray-800 py-3">
            <div className="flex flex-col space-y-1">
              {navItems.map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  onClick={() => handleNavigation(id)}
                  className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-all text-left ${
                    activeTab === id
                      ? 'bg-blue-50 text-blue-700 dark:bg-blue-600/20 dark:text-blue-400'
                      : 'text-slate-600 hover:bg-slate-100 dark:text-gray-400 dark:hover:bg-gray-800/60 dark:hover:text-gray-200'
                  }`}
                >
                  <Icon className="w-4 h-4 mr-3 flex-shrink-0" />
                  <span>{label}</span>
                </button>
              ))}
            </div>

            {/* Mobile User Info */}
            <div className="mt-3 pt-3 border-t border-slate-200 dark:border-gray-800">
              <div className="flex items-center justify-between px-4 py-2 text-xs">
                <div className="flex items-center space-x-2 min-w-0">
                  <span className="relative flex h-2 w-2 flex-shrink-0">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </span>

                  <span className="text-slate-700 dark:text-gray-300 font-medium truncate">
                    {currentUser?.username || 'Analyst'}
                  </span>
                </div>

                <span className="text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-950/80 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-800/60 text-[10px] font-semibold whitespace-nowrap ml-2">
                  {currentUser?.role || 'Security Analyst'}
                </span>
              </div>
            </div>
          </div>
        )}

      </div>
    </nav>
  );
}