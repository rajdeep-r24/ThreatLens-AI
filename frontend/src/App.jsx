import React, { useState } from 'react';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import UploadPage from './pages/UploadPage';
import AnalysisResultPage from './pages/AnalysisResultPage';

export default function App() {
  const [currentUser, setCurrentUser] = useState({
    username: 'analyst_jane',
    email: 'jane@threatlens.ai',
    role: 'Security Analyst'
  });
  const [activeTab, setActiveTab] = useState('dashboard'); // 'dashboard' | 'upload' | 'results'
  const [theme, setTheme] = useState(
    localStorage.getItem('theme') || 'light'
  );
  
  React.useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const [selectedFileId, setSelectedFileId] = useState(1);

  const handleLoginSuccess = (user) => {
    setCurrentUser(user);
    setActiveTab('dashboard');
  };

  const handleLogout = () => {
    setCurrentUser(null);
  };

  const handleSelectFile = (fileId) => {
    setSelectedFileId(fileId);
    setActiveTab('results');
  };

  const handleUploadComplete = (fileId) => {
    setSelectedFileId(fileId);
    setActiveTab('results');
  };

  if (!currentUser) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className={`min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-300 flex flex-col transition-colors duration-200`}>
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentUser={currentUser}
        onLogout={handleLogout}
        theme={theme}
        toggleTheme={toggleTheme}
      />

      <main className="flex-grow">
        {activeTab === 'dashboard' && (
          <DashboardPage
            onSelectFile={handleSelectFile}
            onNavigateUpload={() => setActiveTab('upload')}
          />
        )}

        {activeTab === 'upload' && (
          <UploadPage onUploadComplete={handleUploadComplete} />
        )}

        {activeTab === 'results' && (
          <AnalysisResultPage fileId={selectedFileId} />
        )}
      </main>

      <footer className="border-t border-slate-200 dark:border-slate-800/50 bg-white dark:bg-slate-950 py-6 text-center text-sm text-slate-500 dark:text-slate-400 transition-colors">
        &copy; {new Date().getFullYear()} ThreatLens AI. All rights reserved.
      </footer>
    </div>
  );
}
