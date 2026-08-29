import React, { useState, useEffect } from 'react';
import { fetchFileDetail } from '../services/api';
import { ShieldAlert, ShieldCheck, Copy, Check, FileCode, Terminal, Globe, AlertTriangle, Cpu, Layers } from 'lucide-react';

export default function AnalysisResultPage({ fileId }) {
  const [fileData, setFileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [copiedHash, setCopiedHash] = useState(null);

  useEffect(() => {
    async function loadDetail() {
      setLoading(true);
      const data = await fetchFileDetail(fileId || 1);
      setFileData(data);
      setLoading(false);
    }
    loadDetail();
  }, [fileId]);

  const copyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text);
    setCopiedHash(label);
    setTimeout(() => setCopiedHash(null), 2000);
  };

  if (loading || !fileData) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <div className="inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm text-gray-400 mt-3">Loading static analysis report...</p>
      </div>
    );
  }

  const analysis = fileData.analysis_result || {};
  const yaraList = fileData.yara_results || [];
  const score = analysis.risk_score ?? 0;
  const isHigh = score >= 60;
  const isMedium = score >= 30 && score < 60;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Threat Alert Card */}
      <div className={`rounded-2xl border p-6 ${
        isHigh
          ? 'bg-red-950/20 border-red-500/40 cyber-glow-red'
          : isMedium
          ? 'bg-amber-950/20 border-amber-500/40'
          : 'bg-emerald-950/20 border-emerald-500/40'
      }`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center space-x-3">
              <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${
                isHigh
                  ? 'bg-red-500/20 text-red-400 border-red-500/40'
                  : isMedium
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                  : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
              }`}>
                {analysis.threat_classification || 'Malware Classification'}
              </span>
              <span className="text-xs text-gray-400 font-mono">
                Target: {fileData.filename}
              </span>
            </div>

            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              Static Analysis & Threat Report
            </h1>

            <p className="text-sm text-gray-300 flex items-center">
              <AlertTriangle className="w-4 h-4 mr-1.5 text-amber-400 flex-shrink-0" />
              <strong>Recommended Action:</strong>&nbsp;{analysis.recommended_action || 'Escalate for Security Analyst Review'}
            </p>
          </div>

          {/* Risk Gauge Score Box */}
          <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 text-center min-w-[200px]">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block">
              Generated Risk Score
            </span>
            <div className={`text-4xl font-black mt-2 font-mono ${
              isHigh ? 'text-red-400' : isMedium ? 'text-amber-400' : 'text-emerald-400'
            }`}>
              {score}<span className="text-lg text-gray-500">/100</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-2 mt-3 overflow-hidden">
              <div
                className={`h-full ${isHigh ? 'bg-red-500' : isMedium ? 'bg-amber-500' : 'bg-emerald-500'}`}
                style={{ width: `${score}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* File Hashes Bar */}
      <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex items-center justify-between bg-gray-900/60 p-3 rounded-lg border border-gray-800">
          <div>
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest block">MD5 Hash</span>
            <span className="font-mono text-xs text-gray-200">{fileData.md5_hash}</span>
          </div>
          <button
            onClick={() => copyToClipboard(fileData.md5_hash, 'md5')}
            className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-800 rounded transition-colors"
            title="Copy MD5"
          >
            {copiedHash === 'md5' ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>

        <div className="flex items-center justify-between bg-gray-900/60 p-3 rounded-lg border border-gray-800">
          <div>
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest block">SHA-256 Hash</span>
            <span className="font-mono text-xs text-gray-200 truncate max-w-[280px] sm:max-w-none block">{fileData.sha256_hash}</span>
          </div>
          <button
            onClick={() => copyToClipboard(fileData.sha256_hash, 'sha256')}
            className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-800 rounded transition-colors"
            title="Copy SHA-256"
          >
            {copiedHash === 'sha256' ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Analysis Tabs */}
      <div className="bg-[#111827] border border-gray-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="flex border-b border-gray-800 bg-gray-900/40 overflow-x-auto">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-5 py-3 text-sm font-medium flex items-center space-x-2 border-b-2 whitespace-nowrap transition-colors ${
              activeTab === 'overview'
                ? 'border-blue-500 text-blue-400 bg-blue-950/20'
                : 'border-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            <FileCode className="w-4 h-4" />
            <span>File & PE Metadata</span>
          </button>

          <button
            onClick={() => setActiveTab('yara')}
            className={`px-5 py-3 text-sm font-medium flex items-center space-x-2 border-b-2 whitespace-nowrap transition-colors ${
              activeTab === 'yara'
                ? 'border-blue-500 text-blue-400 bg-blue-950/20'
                : 'border-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            <ShieldAlert className="w-4 h-4 text-amber-400" />
            <span>YARA Rule Matches ({yaraList.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('strings')}
            className={`px-5 py-3 text-sm font-medium flex items-center space-x-2 border-b-2 whitespace-nowrap transition-colors ${
              activeTab === 'strings'
                ? 'border-blue-500 text-blue-400 bg-blue-950/20'
                : 'border-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            <Terminal className="w-4 h-4" />
            <span>Extracted Strings & APIs</span>
          </button>

          <button
            onClick={() => setActiveTab('network')}
            className={`px-5 py-3 text-sm font-medium flex items-center space-x-2 border-b-2 whitespace-nowrap transition-colors ${
              activeTab === 'network'
                ? 'border-blue-500 text-blue-400 bg-blue-950/20'
                : 'border-transparent text-gray-400 hover:text-gray-200'
            }`}
          >
            <Globe className="w-4 h-4 text-cyan-400" />
            <span>Network Indicators</span>
          </button>
        </div>

        {/* Tab Contents */}
        <div className="p-6 space-y-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-900/60 p-4 rounded-xl border border-gray-800">
                  <span className="text-xs text-gray-400 block font-semibold">File Format / Architecture</span>
                  <span className="text-sm font-mono text-white mt-1 block">{fileData.file_type || 'Executable (PE32)'}</span>
                </div>
                <div className="bg-gray-900/60 p-4 rounded-xl border border-gray-800">
                  <span className="text-xs text-gray-400 block font-semibold">File Size</span>
                  <span className="text-sm font-mono text-white mt-1 block">{(fileData.file_size / 1024).toFixed(2)} KB</span>
                </div>
                <div className="bg-gray-900/60 p-4 rounded-xl border border-gray-800">
                  <span className="text-xs text-gray-400 block font-semibold">Upload Timestamp</span>
                  <span className="text-sm font-mono text-white mt-1 block">{new Date(fileData.uploaded_at).toLocaleString()}</span>
                </div>
              </div>

              {analysis.pe_headers && (
                <div className="bg-gray-900/80 p-5 rounded-xl border border-gray-800 space-y-3">
                  <h3 className="text-sm font-bold text-gray-200 flex items-center">
                    <Cpu className="w-4 h-4 mr-2 text-blue-400" />
                    PE Header Specifications
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
                    <div className="bg-gray-950 p-2.5 rounded border border-gray-800">
                      <span className="text-gray-500 block">Entry Point</span>
                      <span className="text-blue-300">{analysis.pe_headers.entry_point || '0x00401000'}</span>
                    </div>
                    <div className="bg-gray-950 p-2.5 rounded border border-gray-800">
                      <span className="text-gray-500 block">Subsystem</span>
                      <span className="text-blue-300">{analysis.pe_headers.subsystem || 'Windows GUI'}</span>
                    </div>
                    <div className="bg-gray-950 p-2.5 rounded border border-gray-800">
                      <span className="text-gray-500 block">Sections Count</span>
                      <span className="text-blue-300">{analysis.pe_headers.number_of_sections || 5}</span>
                    </div>
                    <div className="bg-gray-950 p-2.5 rounded border border-gray-800">
                      <span className="text-gray-500 block">Image Base</span>
                      <span className="text-blue-300">{analysis.pe_headers.image_base || '0x00400000'}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'yara' && (
            <div className="space-y-4">
              <h3 className="text-sm font-bold text-gray-200 flex items-center">
                <ShieldAlert className="w-4 h-4 mr-2 text-amber-400" />
                Matched YARA Signature Rules
              </h3>

              {yaraList.length === 0 ? (
                <div className="p-8 text-center bg-gray-900/40 rounded-xl border border-gray-800 text-gray-400 text-sm">
                  No YARA rule matches detected for this sample.
                </div>
              ) : (
                yaraList.map((yara) => (
                  <div key={yara.id} className="bg-gray-900/80 border border-amber-900/40 rounded-xl p-5 space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="font-mono text-sm font-bold text-amber-400">{yara.rule_name}</span>
                        <span className="text-[10px] bg-red-950 text-red-400 border border-red-800 px-2 py-0.5 rounded font-semibold uppercase">
                          Severity: {yara.severity}
                        </span>
                      </div>
                      <span className="text-xs text-gray-500 font-mono">Rule ID #{yara.id}</span>
                    </div>

                    {yara.tags && yara.tags.length > 0 && (
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-gray-400">Tags:</span>
                        {yara.tags.map((tag, i) => (
                          <span key={i} className="text-[10px] bg-gray-800 text-gray-300 px-2 py-0.5 rounded border border-gray-700 font-mono">
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}

                    {yara.matched_strings && yara.matched_strings.length > 0 && (
                      <div className="bg-gray-950 p-3 rounded-lg border border-gray-800">
                        <span className="text-[11px] text-gray-400 font-semibold block mb-1">Matched String Sequences:</span>
                        {yara.matched_strings.map((str, idx) => (
                          <code key={idx} className="block text-xs font-mono text-amber-300/90 py-0.5">
                            {str}
                          </code>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === 'strings' && (
            <div className="space-y-5">
              <div>
                <h3 className="text-sm font-bold text-gray-200 mb-2 flex items-center">
                  <Layers className="w-4 h-4 mr-2 text-blue-400" />
                  Imported APIs & DLL Calls
                </h3>
                <div className="bg-gray-950 p-4 rounded-xl border border-gray-800 max-h-48 overflow-y-auto space-y-1">
                  {(analysis.suspicious_apis || []).map((api, idx) => (
                    <div key={idx} className="font-mono text-xs text-red-300/90 flex items-center space-x-2">
                      <span className="text-gray-600 text-[10px]">{idx + 1}.</span>
                      <span>{api}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-sm font-bold text-gray-200 mb-2 flex items-center">
                  <Terminal className="w-4 h-4 mr-2 text-cyan-400" />
                  Extracted Suspicious Commands & Strings
                </h3>
                <div className="bg-gray-950 p-4 rounded-xl border border-gray-800 max-h-48 overflow-y-auto space-y-1">
                  {(analysis.extracted_strings || []).map((str, idx) => (
                    <div key={idx} className="font-mono text-xs text-cyan-300/90 break-all py-0.5">
                      &gt; {str}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'network' && (
            <div className="space-y-4">
              <h3 className="text-sm font-bold text-gray-200 flex items-center">
                <Globe className="w-4 h-4 mr-2 text-cyan-400" />
                Detected Network Indicators & C2 Callback References
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-900/60 p-4 rounded-xl border border-gray-800">
                  <span className="text-xs text-gray-400 font-semibold block mb-2">Embedded URLs</span>
                  {(analysis.network_indicators?.urls || []).length === 0 ? (
                    <span className="text-xs text-gray-500 italic">No embedded URLs detected.</span>
                  ) : (
                    analysis.network_indicators.urls.map((url, i) => (
                      <div key={i} className="font-mono text-xs text-cyan-400 bg-gray-950 p-2 rounded mb-1.5 border border-gray-800 break-all">
                        {url}
                      </div>
                    ))
                  )}
                </div>

                <div className="bg-gray-900/60 p-4 rounded-xl border border-gray-800">
                  <span className="text-xs text-gray-400 font-semibold block mb-2">Embedded IP Addresses</span>
                  {(analysis.network_indicators?.ips || []).length === 0 ? (
                    <span className="text-xs text-gray-500 italic">No IP addresses detected.</span>
                  ) : (
                    analysis.network_indicators.ips.map((ip, i) => (
                      <div key={i} className="font-mono text-xs text-amber-400 bg-gray-950 p-2 rounded mb-1.5 border border-gray-800">
                        {ip}
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
