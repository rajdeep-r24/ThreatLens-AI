import React, { useCallback, useEffect, useMemo, useState } from 'react';
import {
  fetchDashboardStats,
  fetchFileList
} from '../services/api';

import {
  ShieldAlert,
  ShieldCheck,
  FileSearch,
  Zap,
  AlertTriangle,
  ArrowUpRight,
  CheckCircle2,
  FileCode,
  RefreshCw,
  Activity,
  TrendingUp,
  BrainCircuit,
  Binary
} from 'lucide-react';

import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  LineChart,
  Line
} from 'recharts';

export default function DashboardPage({ onSelectFile, onNavigateUpload }) {
  const [stats, setStats] = useState(null);
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [lastUpdated, setLastUpdated] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  // ---------------------------------------------------------
  // Load dashboard data
  // ---------------------------------------------------------

  const loadData = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      setError('');

      const [statsData, filesData] = await Promise.all([
        fetchDashboardStats(),
        fetchFileList()
      ]);

      setStats(statsData);
      setFiles(Array.isArray(filesData) ? filesData : []);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Dashboard loading error:', err);
      setError('Unable to load monitoring data.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    loadData();
  }, [loadData]);

  // Automatic refresh every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      loadData(true);
    }, 30000);

    return () => clearInterval(interval);
  }, [loadData]);

  // ---------------------------------------------------------
  // Malware distribution
  // ---------------------------------------------------------

  const malwareDistribution = useMemo(() => {
    const counts = {};

    files.forEach((file) => {
      const classification =
        file.analysis_result?.threat_classification || 'Benign / Clean';

      counts[classification] = (counts[classification] || 0) + 1;
    });

    return Object.entries(counts).map(([name, value]) => ({
      name,
      value
    }));
  }, [files]);

  // ---------------------------------------------------------
  // Risk level distribution
  // ---------------------------------------------------------

  const riskDistribution = useMemo(() => {
    const levels = {
      Critical: 0,
      High: 0,
      Medium: 0,
      Low: 0
    };

    files.forEach((file) => {
      const score = Number(file.analysis_result?.risk_score ?? 0);

      if (score >= 80) {
        levels.Critical += 1;
      } else if (score >= 60) {
        levels.High += 1;
      } else if (score >= 30) {
        levels.Medium += 1;
      } else {
        levels.Low += 1;
      }
    });

    return Object.entries(levels).map(([name, value]) => ({
      name,
      value
    }));
  }, [files]);

  // ---------------------------------------------------------
  // Threat trend
  // ---------------------------------------------------------

  const threatTrend = useMemo(() => {
    const grouped = {};

    files.forEach((file) => {
      const score = Number(file.analysis_result?.risk_score ?? 0);

      const dateValue =
        file.analysis_result?.created_at ||
        file.uploaded_at;

      if (!dateValue) return;

      const date = new Date(dateValue);

      if (Number.isNaN(date.getTime())) return;

      const dateKey = date.toLocaleDateString();

      if (!grouped[dateKey]) {
        grouped[dateKey] = {
          date: dateKey,
          threats: 0,
          totalRisk: 0,
          scans: 0
        };
      }

      grouped[dateKey].scans += 1;
      grouped[dateKey].totalRisk += score;

      if (score >= 60) {
        grouped[dateKey].threats += 1;
      }
    });

    return Object.values(grouped)
      .sort((a, b) => new Date(a.date) - new Date(b.date))
      .map((item) => ({
        date: item.date,
        threats: item.threats,
        averageRisk:
          item.scans > 0
            ? Number((item.totalRisk / item.scans).toFixed(1))
            : 0
      }));
  }, [files]);

  // ---------------------------------------------------------
  // Chart values
  // ---------------------------------------------------------

  const malwareColors = [
    '#ef4444',
    '#f59e0b',
    '#06b6d4',
    '#8b5cf6',
    '#22c55e',
    '#ec4899'
  ];

  const riskColors = {
    Critical: '#dc2626',
    High: '#ef4444',
    Medium: '#f59e0b',
    Low: '#22c55e'
  };

  // ---------------------------------------------------------
  // Loading state
  // ---------------------------------------------------------

  if (loading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center">
        <div className="flex items-center gap-3 text-slate-600 dark:text-gray-300">
          <RefreshCw className="w-5 h-5 animate-spin text-blue-500 dark:text-blue-400" />
          <span>Loading live security monitoring data...</span>
        </div>
      </div>
    );
  }

  // ---------------------------------------------------------
  // Dashboard
  // ---------------------------------------------------------

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200 dark:border-gray-800">

        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            Security Analyst Intelligence Dashboard

            <span className="text-xs bg-emerald-50 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-300 dark:border-emerald-500/30 px-2.5 py-0.5 rounded-full font-mono font-medium">
              Live Monitoring
            </span>
          </h1>

          <p className="text-sm text-slate-600 dark:text-gray-400 mt-1">
            Dual-engine threat detection: Machine learning behavioral models, static PE analysis, and real-time YARA matching.
          </p>

          {lastUpdated && (
            <div className="text-xs text-slate-500 dark:text-gray-400 mt-2">
              Last synchronized: {lastUpdated.toLocaleTimeString()}
            </div>
          )}
        </div>

        <div className="flex items-center gap-3">

          <button
            onClick={() => loadData(true)}
            disabled={refreshing}
            className="border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:bg-slate-50 dark:hover:bg-gray-800 text-slate-700 dark:text-gray-300 px-3.5 py-2.5 rounded-xl transition-all flex items-center gap-2 text-sm shadow-sm disabled:opacity-50"
          >
            <RefreshCw
              className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`}
            />
            <span>Refresh</span>
          </button>

          <button
            onClick={onNavigateUpload}
            className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2.5 rounded-xl shadow-md hover:shadow-blue-500/20 transition-all flex items-center justify-center gap-2 text-sm"
          >
            <Zap className="w-4 h-4" />
            <span>Upload Sample for Scan</span>
          </button>

        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/30 text-red-700 dark:text-red-400 rounded-xl px-4 py-3 text-sm">
          {error}
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

        {/* Total scans */}
        <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-xl p-5 shadow-sm transition-colors">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 uppercase tracking-wider">
              Files Analyzed
            </span>

            <div className="p-2 bg-blue-50 dark:bg-blue-500/10 rounded-lg text-blue-600 dark:text-blue-400">
              <FileSearch className="w-5 h-5" />
            </div>
          </div>

          <div className="text-3xl font-extrabold text-slate-900 dark:text-white mt-3">
            {stats?.total_scans ?? 0}
          </div>

          <div className="text-xs text-slate-500 dark:text-gray-400 mt-2 flex items-center">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 mr-1" />
            {stats?.completed_scans ?? 0} samples inspected
          </div>
        </div>

        {/* AI Malicious Detections */}
        <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-xl p-5 shadow-sm transition-colors">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 uppercase tracking-wider">
              AI Malicious Detections
            </span>

            <div className="p-2 bg-red-50 dark:bg-red-500/10 rounded-lg text-red-600 dark:text-red-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
          </div>

          <div className="text-3xl font-extrabold text-red-600 dark:text-red-400 mt-3">
            {stats?.malicious_threats ?? 0}
          </div>

          <div className="text-xs text-red-600 dark:text-red-400/80 mt-2 flex items-center">
            <AlertTriangle className="w-3.5 h-3.5 mr-1" />
            High/Critical risk (&gt;60/100)
          </div>
        </div>

        {/* YARA */}
        <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-xl p-5 shadow-sm transition-colors">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 uppercase tracking-wider">
              YARA Signature Hits
            </span>

            <div className="p-2 bg-amber-50 dark:bg-amber-500/10 rounded-lg text-amber-600 dark:text-amber-400">
              <Zap className="w-5 h-5" />
            </div>
          </div>

          <div className="text-3xl font-extrabold text-amber-600 dark:text-amber-400 mt-3">
            {stats?.yara_matches ?? 0}
          </div>

          <div className="text-xs text-slate-500 dark:text-gray-400 mt-2">
            Active rule repository: {stats?.active_rules ?? 48} rules
          </div>
        </div>

        {/* Average risk */}
        <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-xl p-5 shadow-sm transition-colors">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 uppercase tracking-wider">
              Mean Threat Score
            </span>

            <div className="p-2 bg-cyan-50 dark:bg-cyan-500/10 rounded-lg text-cyan-600 dark:text-cyan-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
          </div>

          <div className="text-3xl font-extrabold text-cyan-600 dark:text-cyan-400 mt-3">
            {stats?.avg_risk_score ?? 0} / 100
          </div>

          <div className="text-xs text-slate-500 dark:text-gray-400 mt-2">
            Dual-engine normalized risk
          </div>
        </div>

      </div>

      {/* Threat Trend */}
      <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">

        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
              AI Threat Detection & Risk Trend
            </h2>
          </div>

          <span className="text-xs text-slate-500 dark:text-gray-400">
            Telemetry samples with risk score ≥ 60
          </span>
        </div>

        {threatTrend.length > 0 ? (
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={threatTrend}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-gray-800" />

                <XAxis
                  dataKey="date"
                  stroke="#94a3b8"
                  tick={{ fontSize: 12 }}
                />

                <YAxis
                  allowDecimals={false}
                  stroke="#94a3b8"
                  tick={{ fontSize: 12 }}
                />

                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--tooltip-bg, #1e293b)',
                    borderColor: 'var(--tooltip-border, #334155)',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />

                <Legend />

                <Line
                  type="monotone"
                  dataKey="threats"
                  name="Threats Identified"
                  stroke="#ef4444"
                  strokeWidth={3}
                  dot={{ r: 5 }}
                  activeDot={{ r: 7 }}
                />

                <Line
                  type="monotone"
                  dataKey="averageRisk"
                  name="Mean Risk Score"
                  stroke="#06b6d4"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                />

              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="h-72 flex items-center justify-center text-slate-400 dark:text-gray-500">
            No trend data available.
          </div>
        )}

      </div>

      {/* Distribution Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Malware distribution */}
        <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">

          <div className="flex items-center gap-2 mb-4">
            <Activity className="w-5 h-5 text-red-500 dark:text-red-400" />

            <div>
              <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
                Threat Classification Distribution
              </h2>

              <p className="text-xs text-slate-500 dark:text-gray-400">
                AI and heuristic classification of analyzed artifacts
              </p>
            </div>
          </div>

          {malwareDistribution.length > 0 ? (
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>

                  <Pie
                    data={malwareDistribution}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={90}
                    innerRadius={45}
                    paddingAngle={3}
                    label={({ percent }) =>
                      `${(percent * 100).toFixed(0)}%`
                    }
                  >
                    {malwareDistribution.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={malwareColors[index % malwareColors.length]}
                      />
                    ))}
                  </Pie>

                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--tooltip-bg, #1e293b)',
                      borderColor: 'var(--tooltip-border, #334155)',
                      borderRadius: '8px',
                      color: '#fff'
                    }}
                  />

                  <Legend />

                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-72 flex items-center justify-center text-slate-400 dark:text-gray-500">
              No classification data available.
            </div>
          )}

        </div>

        {/* Risk distribution */}
        <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">

          <div className="flex items-center gap-2 mb-4">
            <ShieldAlert className="w-5 h-5 text-amber-500 dark:text-amber-400" />

            <div>
              <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
                Risk Severity Breakdown
              </h2>

              <p className="text-xs text-slate-500 dark:text-gray-400">
                Segmented by dual-engine threat scores
              </p>
            </div>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskDistribution}>

                <CartesianGrid
                  strokeDasharray="3 3"
                  className="stroke-slate-200 dark:stroke-gray-800"
                />

                <XAxis
                  dataKey="name"
                  stroke="#94a3b8"
                  tick={{ fontSize: 12 }}
                />

                <YAxis
                  allowDecimals={false}
                  stroke="#94a3b8"
                  tick={{ fontSize: 12 }}
                />

                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--tooltip-bg, #1e293b)',
                    borderColor: 'var(--tooltip-border, #334155)',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />

                <Bar
                  dataKey="value"
                  name="Files"
                  radius={[6, 6, 0, 0]}
                >
                  {riskDistribution.map((entry) => (
                    <Cell
                      key={entry.name}
                      fill={riskColors[entry.name]}
                    />
                  ))}
                </Bar>

              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-2 text-xs">
            <div className="text-red-600 dark:text-red-400 font-medium">
              Critical: 80–100
            </div>

            <div className="text-red-500 dark:text-red-300 font-medium">
              High: 60–79
            </div>

            <div className="text-amber-600 dark:text-amber-400 font-medium">
              Medium: 30–59
            </div>

            <div className="text-emerald-600 dark:text-emerald-400 font-medium">
              Low: 0–29
            </div>
          </div>

        </div>

      </div>

      {/* Recent Threats */}
      <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-2xl overflow-hidden shadow-sm">

        <div className="px-6 py-5 border-b border-slate-200 dark:border-gray-800 flex items-center justify-between">

          <div className="flex items-center gap-2">
            <FileCode className="w-5 h-5 text-blue-600 dark:text-blue-400" />

            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
              Recent Artifacts & Threat Intelligence Results
            </h2>
          </div>

          <span className="text-xs text-slate-500 dark:text-gray-400 font-mono">
            Showing {files.length} records
          </span>

        </div>

        <div className="overflow-x-auto">

          <table className="w-full text-left text-sm text-slate-700 dark:text-gray-300">

            <thead className="bg-slate-50 dark:bg-gray-900/60 text-xs text-slate-500 dark:text-gray-400 uppercase tracking-wider border-b border-slate-200 dark:border-gray-800">

              <tr>
                <th className="px-6 py-3.5">
                  Filename
                </th>

                <th className="px-6 py-3.5">
                  SHA-256 Hash
                </th>

                <th className="px-6 py-3.5">
                  Threat Classification
                </th>

                <th className="px-6 py-3.5">
                  Threat Score
                </th>

                <th className="px-6 py-3.5">
                  Severity
                </th>

                <th className="px-6 py-3.5">
                  YARA Hits
                </th>

                <th className="px-6 py-3.5 text-right">
                  Action
                </th>
              </tr>

            </thead>

            <tbody className="divide-y divide-slate-100 dark:divide-gray-800/60">

              {files.map((file) => {

                const score =
                  Number(file.analysis_result?.risk_score ?? 0);

                const riskLevel =
                  score >= 80
                    ? 'Critical'
                    : score >= 60
                    ? 'High'
                    : score >= 30
                    ? 'Medium'
                    : 'Low';

                const riskClass =
                  riskLevel === 'Critical'
                    ? 'bg-red-50 text-red-700 border-red-200 dark:bg-red-600/20 dark:text-red-300 dark:border-red-500/40'
                    : riskLevel === 'High'
                    ? 'bg-red-50 text-red-600 border-red-200 dark:bg-red-500/10 dark:text-red-400 dark:border-red-500/30'
                    : riskLevel === 'Medium'
                    ? 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-500/10 dark:text-amber-400 dark:border-amber-500/30'
                    : 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/30';

                return (
                  <tr
                    key={file.id}
                    className="hover:bg-slate-50 dark:hover:bg-gray-800/40 transition-colors"
                  >

                    <td className="px-6 py-4 font-medium text-slate-900 dark:text-white">

                      <div className="flex items-center space-x-2">

                        <FileCode className="w-4 h-4 text-slate-400 dark:text-gray-400 flex-shrink-0" />

                        <span className="font-semibold">
                          {file.filename}
                        </span>

                      </div>

                    </td>

                    <td
                      className="px-6 py-4 font-mono text-xs text-slate-500 dark:text-gray-400 max-w-[200px] truncate"
                      title={file.sha256_hash}
                    >
                      {file.sha256_hash || 'Calculating...'}
                    </td>

                    <td className="px-6 py-4">

                      <span
                        className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold border ${riskClass}`}
                      >
                        {file.analysis_result?.threat_classification ||
                          'Analyzing'}
                      </span>

                    </td>

                    <td className="px-6 py-4 font-mono">

                      <div className="flex items-center space-x-2">

                        <div className="w-16 bg-slate-200 dark:bg-gray-800 rounded-full h-2 overflow-hidden">

                          <div
                            className={`h-full ${
                              score >= 60
                                ? 'bg-red-500'
                                : score >= 30
                                ? 'bg-amber-500'
                                : 'bg-emerald-500'
                            }`}
                            style={{
                              width: `${Math.min(score, 100)}%`
                            }}
                          />

                        </div>

                        <span className="text-xs font-bold text-slate-800 dark:text-gray-200">
                          {score}/100
                        </span>

                      </div>

                    </td>

                    <td className="px-6 py-4">

                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded border text-xs font-semibold ${riskClass}`}
                      >
                        {riskLevel}
                      </span>

                    </td>

                    <td className="px-6 py-4">

                      <span className="text-xs bg-slate-100 dark:bg-gray-800 text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-gray-700 px-2 py-0.5 rounded font-mono">
                        {file.yara_results?.length || 0} matched
                      </span>

                    </td>

                    <td className="px-6 py-4 text-right">

                      <button
                        onClick={() => onSelectFile(file.id)}
                        className="inline-flex items-center text-xs font-semibold text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800/60 px-3 py-1.5 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/60 transition-all shadow-sm"
                      >

                        <span>
                          View Report
                        </span>

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