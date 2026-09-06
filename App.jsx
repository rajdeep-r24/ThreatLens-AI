import React, { useState } from 'react';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import UploadPage from './pages/UploadPage';
import AnalysisResultPage from './pages/AnalysisResultPage';
import AlertsReportsPage from './pages/AlertsReportsPage';

export default function App() {
  const [currentUser, setCurrentUser] = useState({
    username: 'analyst_jane',
    email: 'jane@threatlens.ai',
    role: 'Security Analyst'
  });

  const [activeTab, setActiveTab] = useState('dashboard');

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
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 flex flex-col">

      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentUser={currentUser}
        onLogout={handleLogout}
      />

      <main className="flex-grow">

        {activeTab === 'dashboard' && (
          <DashboardPage
            onSelectFile={handleSelectFile}
            onNavigateUpload={() => setActiveTab('upload')}
          />
        )}

        {activeTab === 'upload' && (
          <UploadPage
            onUploadComplete={handleUploadComplete}
          />
        )}

        {activeTab === 'results' && (
          <AnalysisResultPage
            fileId={selectedFileId}
          />
        )}

        {activeTab === 'alerts' && (
          <AlertsReportsPage />
        )}

      </main>

      <footer className="border-t border-gray-800 bg-[#0B0F19] py-4 text-center text-xs text-gray-500 font-mono">
        ThreatLens AI Platform • Member 5 — Alerts & Malware Reports
      </footer>

    </div>
  );
}