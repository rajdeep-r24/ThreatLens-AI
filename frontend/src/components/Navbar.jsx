import React, { useState } from 'react';
import {
  Shield,
  LayoutDashboard,
  UploadCloud,
  FileText,
  LogOut,
  Menu,
  X
} from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  currentUser,
  onLogout
}) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleNavigation = (tab) => {
    setActiveTab(tab);
    setMobileMenuOpen(false);
  };

  const navItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: LayoutDashboard
    },
    {
      id: 'upload',
      label: 'Upload & Scan',
      icon: UploadCloud
    },
    {
      id: 'results',
      label: 'Static Analysis Reports',
      icon: FileText
    }
  ];

  return (
    <nav className="bg-[#111827] border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Main Navbar */}
        <div className="flex items-center justify-between min-h-16 py-2">

          {/* Brand Logo */}
          <div
            className="flex items-center space-x-3 cursor-pointer min-w-0"
            onClick={() => handleNavigation('dashboard')}
          >
            <div className="flex-shrink-0 p-2 bg-blue-600/20 border border-blue-500/40 rounded-lg text-blue-400 cyber-glow-blue">
              <Shield className="w-6 h-6" />
            </div>

            <div className="min-w-0">
              <span className="block text-lg sm:text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent truncate">
                ThreatLens AI
              </span>

              <span className="hidden sm:block text-[10px] text-gray-400 uppercase tracking-widest font-mono truncate">
                Malware Detection & Analytics
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => handleNavigation(id)}
                className={`flex items-center px-3 lg:px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === id
                    ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
                }`}
              >
                <Icon className="w-4 h-4 mr-2 flex-shrink-0" />
                <span>{label}</span>
              </button>
            ))}
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-2 sm:space-x-3">

            {/* User Profile */}
            <div className="hidden lg:flex items-center text-xs space-x-2 px-3 py-1.5 bg-gray-800/80 rounded-full border border-gray-700 max-w-xs">
              <span className="relative flex h-2 w-2 flex-shrink-0">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>

              <span className="text-gray-300 font-medium truncate">
                {currentUser?.username || 'Analyst'}
              </span>

              <span className="text-blue-400 bg-blue-950/80 px-2 py-0.5 rounded border border-blue-800/60 text-[10px] font-semibold whitespace-nowrap">
                {currentUser?.role || 'Security Analyst'}
              </span>
            </div>

            {/* Logout */}
            <button
              onClick={onLogout}
              title="Logout"
              aria-label="Logout"
              className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-950/40 rounded-lg transition-colors border border-transparent hover:border-red-900/40 flex-shrink-0"
            >
              <LogOut className="w-5 h-5" />
            </button>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen((prev) => !prev)}
              aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
              aria-expanded={mobileMenuOpen}
              className="md:hidden p-2 text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded-lg transition-colors border border-transparent hover:border-gray-700"
            >
              {mobileMenuOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </button>

          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-800 py-3">
            <div className="flex flex-col space-y-1">
              {navItems.map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  onClick={() => handleNavigation(id)}
                  className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-all text-left ${
                    activeTab === id
                      ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
                  }`}
                >
                  <Icon className="w-4 h-4 mr-3 flex-shrink-0" />
                  <span>{label}</span>
                </button>
              ))}
            </div>

            {/* Mobile User Info */}
            <div className="mt-3 pt-3 border-t border-gray-800">
              <div className="flex items-center justify-between px-4 py-2 text-xs">
                <div className="flex items-center space-x-2 min-w-0">
                  <span className="relative flex h-2 w-2 flex-shrink-0">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </span>

                  <span className="text-gray-300 font-medium truncate">
                    {currentUser?.username || 'Analyst'}
                  </span>
                </div>

                <span className="text-blue-400 bg-blue-950/80 px-2 py-0.5 rounded border border-blue-800/60 text-[10px] font-semibold whitespace-nowrap ml-2">
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