import React, { useEffect, useState } from 'react';
import { fetchDashboardStats, fetchFileList } from '../services/api';
import { ShieldAlert, ShieldCheck, FileSearch, Zap, AlertTriangle, ArrowUpRight, CheckCircle2, FileCode } from 'lucide-react';

export default function DashboardPage({ onSelectFile, onNavigateUpload }) {
  const [stats, setStats] = useState(null);
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const sData = await fetchDashboardStats();
      const fData = await fetchFileList();
      setStats(sData);
      setFiles(fData);
      setLoading(false);
    }
    loadData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-gray-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            Security Analyst Dashboard
            <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-0.5 rounded-full font-mono">
              Live Monitoring
            </span>
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Real-time malware analysis overview, static scan results, and YARA signature triggers.
          </p>
        </div>

        <button
          onClick={onNavigateUpload}
          className="bg-blue-600 hover:bg-blue-500 text-white font-medium px-4 py-2.5 rounded-xl shadow-lg hover:shadow-blue-500/20 transition-all flex items-center justify-center space-x-2 text-sm"
        >
          <Zap className="w-4 h-4" />
          <span>Upload New File for Scan</span>
        </button>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Total Files Scanned</span>
            <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
              <FileSearch className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-white mt-3">{stats?.total_scans ?? 0}</div>
          <div className="text-xs text-gray-400 mt-2 flex items-center">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 mr-1" />
            <span>{stats?.completed_scans ?? 0} static scans completed</span>
          </div>
        </div>

        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Malicious Threats</span>
            <div className="p-2 bg-red-500/10 rounded-lg text-red-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-red-400 mt-3">{stats?.malicious_threats ?? 0}</div>
          <div className="text-xs text-red-400/80 mt-2 flex items-center">
            <AlertTriangle className="w-3.5 h-3.5 mr-1" />
            <span>High risk score (&gt;60/100)</span>
          </div>
        </div>

        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">YARA Rule Matches</span>
            <div className="p-2 bg-amber-500/10 rounded-lg text-amber-400">
              <Zap className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-amber-400 mt-3">{stats?.yara_matches ?? 0}</div>
          <div className="text-xs text-gray-400 mt-2">
            <span>Across {stats?.active_rules ?? 48} active signature rules</span>
          </div>
        </div>

        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Average Threat Score</span>
            <div className="p-2 bg-cyan-500/10 rounded-lg text-cyan-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-cyan-400 mt-3">{stats?.avg_risk_score ?? 0} / 100</div>
          <div className="text-xs text-gray-400 mt-2">
            <span>Normalized risk metric</span>
          </div>
        </div>
      </div>

      {/* Main Content Area: Recent Scans & Analysis Results */}
      <div className="bg-[#111827] border border-gray-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="px-6 py-5 border-b border-gray-800 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FileCode className="w-5 h-5 text-blue-400" />
            <h2 className="text-lg font-semibold text-white">Recent Static Analysis Results</h2>
          </div>
          <span className="text-xs text-gray-400 font-mono">
            Showing {files.length} records
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="bg-gray-900/60 text-xs text-gray-400 uppercase tracking-wider border-b border-gray-800">
              <tr>
                <th className="px-6 py-3.5">Filename</th>
                <th className="px-6 py-3.5">SHA-256 Hash</th>
                <th className="px-6 py-3.5">Classification</th>
                <th className="px-6 py-3.5">Risk Score</th>
                <th className="px-6 py-3.5">YARA Hits</th>
                <th className="px-6 py-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60">
              {files.map((file) => {
                const score = file.analysis_result?.risk_score ?? 0;
                const isHigh = score >= 60;
                const isMedium = score >= 30 && score < 60;

                return (
                  <tr key={file.id} className="hover:bg-gray-800/40 transition-colors">
                    <td className="px-6 py-4 font-medium text-white flex items-center space-x-2">
                      <FileCode className="w-4 h-4 text-gray-400 flex-shrink-0" />
                      <span>{file.filename}</span>
                    </td>

                    <td className="px-6 py-4 font-mono text-xs text-gray-400 max-w-[200px] truncate" title={file.sha256_hash}>
                      {file.sha256_hash || 'Calculating...'}
                    </td>

                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                          isHigh
                            ? 'bg-red-500/10 text-red-400 border-red-500/30'
                            : isMedium
                            ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                            : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                        }`}
                      >
                        {file.analysis_result?.threat_classification || 'Analyzing'}
                      </span>
                    </td>

                    <td className="px-6 py-4 font-mono">
                      <div className="flex items-center space-x-2">
                        <div className="w-16 bg-gray-800 rounded-full h-2 overflow-hidden">
                          <div
                            className={`h-full ${
                              isHigh ? 'bg-red-500' : isMedium ? 'bg-amber-500' : 'bg-emerald-500'
                            }`}
                            style={{ width: `${score}%` }}
                          ></div>
                        </div>
                        <span className={`text-xs font-bold ${isHigh ? 'text-red-400' : isMedium ? 'text-amber-400' : 'text-emerald-400'}`}>
                          {score}/100
                        </span>
                      </div>
                    </td>

                    <td className="px-6 py-4">
                      <span className="text-xs bg-gray-800 text-gray-300 border border-gray-700 px-2 py-0.5 rounded font-mono">
                        {file.yara_results?.length || 0} matched
                      </span>
                    </td>

                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => onSelectFile(file.id)}
                        className="inline-flex items-center text-xs font-medium text-blue-400 hover:text-blue-300 bg-blue-950/40 border border-blue-800/60 px-3 py-1.5 rounded-lg hover:bg-blue-900/60 transition-all"
                      >
                        <span>View Analysis</span>
                        <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
