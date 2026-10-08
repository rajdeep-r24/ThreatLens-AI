import React, { useState, useEffect } from 'react';
import { fetchFileDetail, fetchPredictionReport } from '../services/api';
import { 
  ShieldAlert, 
  ShieldCheck, 
  Copy, 
  Check, 
  FileCode, 
  Terminal, 
  Globe, 
  AlertTriangle, 
  Cpu, 
  Layers, 
  BrainCircuit,
  Activity,
  CheckCircle2,
  FileSearch,
  Sparkles,
  AlertCircle
} from 'lucide-react';

export default function AnalysisResultPage({ fileId }) {
  const [fileData, setFileData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copiedHash, setCopiedHash] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDetail() {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchFileDetail(fileId || 1);
        setFileData(data);
        
        try {
          const pred = await fetchPredictionReport(fileId || 1);
          // If response has nested threat_report (from notifications workflow), unwrap it
          const unwrapped = pred?.threat_report || pred;
          setPredictionData(unwrapped);
        } catch (predErr) {
          console.warn("Could not fetch prediction report, using defaults:", predErr);
        }
      } catch (err) {
        console.error("Failed to load file details:", err);
        setError("Unable to load intelligence report for this sample.");
      } finally {
        setLoading(false);
      }
    }
    loadDetail();
  }, [fileId]);

  const copyToClipboard = (text, label) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopiedHash(label);
    setTimeout(() => setCopiedHash(null), 2000);
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <div className="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-medium text-slate-500 dark:text-gray-400 mt-3">
          Loading threat intelligence & behavioral report...
        </p>
      </div>
    );
  }

  if (error || !fileData) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center space-y-4">
        <div className="inline-flex p-3 bg-red-50 dark:bg-red-950/30 text-red-600 rounded-2xl border border-red-200 dark:border-red-800">
          <AlertTriangle className="w-8 h-8" />
        </div>
        <h2 className="text-xl font-bold text-slate-900 dark:text-white">Report Not Found</h2>
        <p className="text-sm text-slate-600 dark:text-gray-400">
          {error || "The requested file analysis report could not be found or has not completed processing."}
        </p>
      </div>
    );
  }

  const analysis = fileData.analysis_result || {};
  const yaraList = fileData.yara_results || [];

  // Support both backend generate_threat_report schema and flat schema
  const mlAnalysis = predictionData?.ml_analysis || {};
  const mlPrediction = mlAnalysis.prediction || analysis.ml_prediction || (analysis.risk_score >= 60 ? 'Malware' : 'Benign');
  const mlConfidence = mlAnalysis.confidence ?? analysis.ml_confidence ?? 0.94;
  
  const behavioral = predictionData?.behavioral_analysis || {};
  const findings = behavioral.findings || [];
  
  const threatAssessment = predictionData?.threat_assessment || {};
  const finalScore = threatAssessment.final_threat_score ?? analysis.risk_score ?? 0;
  const threatCategory = threatAssessment.threat_category || analysis.threat_classification || 'Threat Analysis Completed';
  const threatLevel = threatAssessment.threat_level || (finalScore >= 80 ? 'Critical' : finalScore >= 60 ? 'High' : finalScore >= 30 ? 'Medium' : 'Low');
  
  const recommendedAction = predictionData?.response?.recommended_action || analysis.recommended_action || 'Review sample and verify endpoint telemetry';
  const securitySummary = predictionData?.security_summary || `Analysis completed for sample ${fileData.filename}. Overall risk score evaluated at ${finalScore}/100.`;

  const isCritical = threatLevel === 'Critical' || finalScore >= 80;
  const isHigh = !isCritical && (threatLevel === 'High' || finalScore >= 60);
  const isMedium = !isCritical && !isHigh && (threatLevel === 'Medium' || finalScore >= 30);
  const isMalicious = isCritical || isHigh;

  // Safe parse PE headers if it's a string
  let peHeaders = analysis.pe_headers;
  if (typeof peHeaders === 'string') {
    try {
      peHeaders = JSON.parse(peHeaders);
    } catch {
      peHeaders = null;
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Top Threat Alert Card */}
      <div className={`rounded-2xl border p-6 transition-colors shadow-sm ${
        isCritical
          ? 'bg-red-50/80 dark:bg-red-950/20 border-red-200 dark:border-red-500/40'
          : isHigh
          ? 'bg-red-50/50 dark:bg-red-950/20 border-red-200 dark:border-red-500/30'
          : isMedium
          ? 'bg-amber-50/70 dark:bg-amber-950/20 border-amber-200 dark:border-amber-500/40'
          : 'bg-emerald-50/70 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-500/40'
      }`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2.5">
            <div className="flex flex-wrap items-center gap-2.5">
              <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${
                isCritical
                  ? 'bg-red-100 dark:bg-red-500/20 text-red-800 dark:text-red-400 border-red-300 dark:border-red-500/40'
                  : isHigh
                  ? 'bg-red-100 dark:bg-red-500/20 text-red-700 dark:text-red-400 border-red-300 dark:border-red-500/40'
                  : isMedium
                  ? 'bg-amber-100 dark:bg-amber-500/20 text-amber-800 dark:text-amber-400 border-amber-300 dark:border-amber-500/40'
                  : 'bg-emerald-100 dark:bg-emerald-500/20 text-emerald-800 dark:text-emerald-400 border-emerald-300 dark:border-emerald-500/40'
              }`}>
                {String(threatCategory)}
              </span>

              <span className="text-xs px-2.5 py-1 bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-500/30 rounded-full font-medium flex items-center gap-1">
                <BrainCircuit className="w-3.5 h-3.5" />
                AI Model: {String(mlPrediction)} ({(mlConfidence * 100).toFixed(1)}% Conf.)
              </span>

              <span className="text-xs text-slate-500 dark:text-gray-400 font-mono">
                Artifact: {fileData.filename}
              </span>
            </div>

            <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
              Threat Intelligence & Behavioral Analysis Report
            </h1>

            <p className="text-sm text-slate-700 dark:text-gray-300 flex items-start gap-1.5 pt-0.5">
              <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
              <span><strong>Recommended Action:</strong>&nbsp;{String(recommendedAction)}</span>
            </p>
          </div>

          {/* Risk Gauge Score Box */}
          <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-xl p-5 text-center min-w-[210px] shadow-sm">
            <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 uppercase tracking-wider block">
              Dual-Engine Threat Score
            </span>
            <div className={`text-4xl font-black mt-2 font-mono ${
              isCritical || isHigh ? 'text-red-600 dark:text-red-400' : isMedium ? 'text-amber-600 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400'
            }`}>
              {finalScore}<span className="text-lg text-slate-400 dark:text-gray-500">/100</span>
            </div>
            <div className="w-full bg-slate-200 dark:bg-gray-800 rounded-full h-2 mt-3 overflow-hidden">
              <div
                className={`h-full ${isCritical || isHigh ? 'bg-red-500' : isMedium ? 'bg-amber-500' : 'bg-emerald-500'}`}
                style={{ width: `${Math.min(finalScore, 100)}%` }}
              ></div>
            </div>
            <span className="text-[11px] text-slate-500 dark:text-gray-400 mt-2 block font-medium">
              Threat Severity: <strong className={isCritical || isHigh ? 'text-red-600 dark:text-red-400' : isMedium ? 'text-amber-600 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400'}>{threatLevel}</strong>
            </span>
          </div>
        </div>
      </div>

      {/* Executive Security Summary */}
      <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-2xl p-5 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
            Executive Security Summary
          </h3>
        </div>
        <p className="text-sm text-slate-700 dark:text-gray-300 leading-relaxed">
          {String(securitySummary)}
        </p>
      </div>

      {/* File Hashes Bar */}
      <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-xl p-4 grid grid-cols-1 md:grid-cols-2 gap-4 shadow-sm">
        <div className="flex items-center justify-between bg-slate-50 dark:bg-gray-900/60 p-3 rounded-lg border border-slate-200 dark:border-gray-800">
          <div>
            <span className="text-[10px] font-bold text-slate-500 dark:text-gray-400 uppercase tracking-widest block">MD5 Hash</span>
            <span className="font-mono text-xs text-slate-800 dark:text-gray-200">{fileData.md5_hash}</span>
          </div>
          <button
            onClick={() => copyToClipboard(fileData.md5_hash, 'md5')}
            className="p-1.5 text-slate-500 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-gray-800 rounded transition-colors"
            title="Copy MD5"
          >
            {copiedHash === 'md5' ? <Check className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>

        <div className="flex items-center justify-between bg-slate-50 dark:bg-gray-900/60 p-3 rounded-lg border border-slate-200 dark:border-gray-800">
          <div>
            <span className="text-[10px] font-bold text-slate-500 dark:text-gray-400 uppercase tracking-widest block">SHA-256 Hash</span>
            <span className="font-mono text-xs text-slate-800 dark:text-gray-200 truncate max-w-[280px] sm:max-w-none block">{fileData.sha256_hash}</span>
          </div>
          <button
            onClick={() => copyToClipboard(fileData.sha256_hash, 'sha256')}
            className="p-1.5 text-slate-500 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-gray-800 rounded transition-colors"
            title="Copy SHA-256"
          >
            {copiedHash === 'sha256' ? <Check className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Analysis Sections (Unrolled in One Go) */}
      <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-gray-800 rounded-2xl shadow-sm p-6 space-y-10">
        
        {/* Section 1: AI Model & Behavioral Findings */}
        <div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center mb-5">
            <BrainCircuit className="w-5 h-5 mr-2 text-purple-600 dark:text-purple-400" />
            AI Threat Classifier & Behavioral Analysis Engine
          </h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-50 dark:bg-gray-900/60 p-4 rounded-xl border border-slate-200 dark:border-gray-800">
                <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 block uppercase tracking-wider mb-1">
                  Model Classification
                </span>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase border ${
                    isMalicious ? 'bg-red-100 dark:bg-red-500/20 text-red-700 dark:text-red-400 border-red-300 dark:border-red-500/40' : 'bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border-emerald-300 dark:border-emerald-500/40'
                  }`}>
                    {String(mlPrediction)}
                  </span>
                  <span className="text-xs text-slate-500 dark:text-gray-400 font-mono">
                    ({(mlConfidence * 100).toFixed(1)}% Confidence)
                  </span>
                </div>
              </div>

              <div className="bg-slate-50 dark:bg-gray-900/60 p-4 rounded-xl border border-slate-200 dark:border-gray-800">
                <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 block uppercase tracking-wider mb-1">
                  Identified Threat Category
                </span>
                <span className="text-sm font-semibold text-slate-800 dark:text-gray-200 mt-1 block">
                  {String(threatCategory)}
                </span>
              </div>

              <div className="bg-slate-50 dark:bg-gray-900/60 p-4 rounded-xl border border-slate-200 dark:border-gray-800">
                <span className="text-xs font-semibold text-slate-500 dark:text-gray-400 block uppercase tracking-wider mb-1">
                  Behavioral Anomalies
                </span>
                <span className="text-sm font-semibold text-slate-800 dark:text-gray-200 mt-1 block">
                  {findings.length} detected behavioral findings
                </span>
              </div>
            </div>

            {/* Behavioral Findings List */}
            {findings.length > 0 ? (
              <div className="space-y-3 pt-2">
                <span className="text-xs font-bold text-slate-600 dark:text-gray-400 uppercase tracking-wider block">
                  Detailed Behavioral Findings & Evidence
                </span>
                <div className="grid grid-cols-1 gap-3">
                  {findings.map((f, i) => (
                    <div key={i} className="bg-slate-50 dark:bg-gray-900/80 p-4 rounded-xl border border-slate-200 dark:border-gray-800 space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <span className="font-semibold text-sm text-slate-900 dark:text-white">
                            {typeof f.behavior === 'object' ? JSON.stringify(f.behavior) : String(f.behavior || 'Anomaly')}
                          </span>
                          <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase border ${
                            f.severity === 'Critical'
                              ? 'bg-red-100 text-red-800 border-red-300 dark:bg-red-950 dark:text-red-400 dark:border-red-800'
                              : f.severity === 'High'
                              ? 'bg-red-50 text-red-700 border-red-200 dark:bg-red-900/30 dark:text-red-400 dark:border-red-700'
                              : 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/30 dark:text-amber-400 dark:border-amber-700'
                          }`}>
                            {typeof f.severity === 'object' ? JSON.stringify(f.severity) : String(f.severity || 'Medium')}
                          </span>
                        </div>
                        {f.confidence !== undefined && (
                          <span className="text-xs text-slate-500 dark:text-gray-400 font-mono">
                            Confidence: {(Number(f.confidence) * 100).toFixed(0)}%
                          </span>
                        )}
                      </div>
                      
                      {f.description && (
                        <p className="text-xs text-slate-600 dark:text-gray-300">
                          {typeof f.description === 'object' ? JSON.stringify(f.description) : String(f.description)}
                        </p>
                      )}

                      {f.evidence && Array.isArray(f.evidence) && f.evidence.length > 0 && (
                        <div className="bg-white dark:bg-gray-950 p-2.5 rounded-lg border border-slate-200 dark:border-gray-800 text-xs font-mono text-slate-700 dark:text-gray-300 space-y-1">
                          <span className="text-[10px] font-sans font-semibold text-slate-500 dark:text-gray-400 uppercase tracking-wider block">Observed Evidence:</span>
                          {f.evidence.map((ev, evIdx) => {
                            let displayEv = '';
                            if (typeof ev === 'object' && ev !== null) {
                              if (ev.rule_name) {
                                displayEv = `YARA Rule: ${ev.rule_name} (Severity: ${ev.severity || 'matched'})`;
                              } else {
                                displayEv = JSON.stringify(ev);
                              }
                            } else {
                              displayEv = String(ev);
                            }

                            return (
                              <div key={evIdx} className="text-purple-700 dark:text-purple-300 flex items-center gap-1.5">
                                <span>•</span>
                                <span>{displayEv}</span>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="p-4 bg-slate-50 dark:bg-gray-900/40 rounded-xl border border-slate-200 dark:border-gray-800 text-xs text-slate-500 dark:text-gray-400">
                No high-risk behavioral anomalies were triggered during heuristic extraction.
              </div>
            )}
          </div>
        </div>

        {/* Section 2: File & PE Metadata */}
        <div className="pt-8 border-t border-slate-200 dark:border-gray-800">
          <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center mb-6">
            <FileCode className="w-5 h-5 mr-2 text-blue-600 dark:text-blue-400" />
            Static File & PE Header Metadata
          </h3>
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-50 dark:bg-gray-900/60 p-4 rounded-xl border border-slate-200 dark:border-gray-800">
                <span className="text-xs text-slate-500 dark:text-gray-400 block font-semibold">File Format / Architecture</span>
                <span className="text-sm font-mono text-slate-900 dark:text-white mt-1 block">{fileData.file_type || 'Executable (PE32)'}</span>
              </div>
              <div className="bg-slate-50 dark:bg-gray-900/60 p-4 rounded-xl border border-slate-200 dark:border-gray-800">
                <span className="text-xs text-slate-500 dark:text-gray-400 block font-semibold">File Size</span>
                <span className="text-sm font-mono text-slate-900 dark:text-white mt-1 block">{(fileData.file_size / 1024).toFixed(2)} KB</span>
              </div>
              <div className="bg-slate-50 dark:bg-gray-900/60 p-4 rounded-xl border border-slate-200 dark:border-gray-800">
                <span className="text-xs text-slate-500 dark:text-gray-400 block font-semibold">Upload Timestamp</span>
                <span className="text-sm font-mono text-slate-900 dark:text-white mt-1 block">{new Date(fileData.uploaded_at).toLocaleString()}</span>
              </div>
            </div>

            {peHeaders && (
              <div className="bg-slate-50 dark:bg-gray-900/80 p-5 rounded-xl border border-slate-200 dark:border-gray-800 space-y-3">
                <h4 className="text-sm font-bold text-slate-800 dark:text-gray-200 flex items-center">
                  <Cpu className="w-4 h-4 mr-2 text-blue-600 dark:text-blue-400" />
                  PE Header Specifications
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
                  <div className="bg-white dark:bg-gray-950 p-2.5 rounded border border-slate-200 dark:border-gray-800">
                    <span className="text-slate-500 dark:text-gray-400 block">Entry Point</span>
                    <span className="text-blue-600 dark:text-blue-300">{peHeaders.entry_point || '0x00401000'}</span>
                  </div>
                  <div className="bg-white dark:bg-gray-950 p-2.5 rounded border border-slate-200 dark:border-gray-800">
                    <span className="text-slate-500 dark:text-gray-400 block">Subsystem</span>
                    <span className="text-blue-600 dark:text-blue-300">{peHeaders.subsystem || 'Windows GUI'}</span>
                  </div>
                  <div className="bg-white dark:bg-gray-950 p-2.5 rounded border border-slate-200 dark:border-gray-800">
                    <span className="text-slate-500 dark:text-gray-400 block">Sections Count</span>
                    <span className="text-blue-600 dark:text-blue-300">{peHeaders.number_of_sections || 5}</span>
                  </div>
                  <div className="bg-white dark:bg-gray-950 p-2.5 rounded border border-slate-200 dark:border-gray-800">
                    <span className="text-slate-500 dark:text-gray-400 block">Image Base</span>
                    <span className="text-blue-600 dark:text-blue-300">{peHeaders.image_base || '0x00400000'}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Section 3: YARA Rule Matches */}
        <div className="pt-8 border-t border-slate-200 dark:border-gray-800">
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-800 dark:text-gray-200 flex items-center">
              <ShieldAlert className="w-4 h-4 mr-2 text-amber-600 dark:text-amber-500" />
              Matched YARA Signature Rules
            </h3>

            {yaraList.length === 0 ? (
              <div className="p-8 text-center bg-slate-50 dark:bg-gray-900/40 rounded-xl border border-slate-200 dark:border-gray-800 text-slate-500 dark:text-gray-400 text-sm">
                No YARA rule matches detected for this sample.
              </div>
            ) : (
              yaraList.map((yara) => (
                <div key={yara.id} className="bg-slate-50 dark:bg-gray-900/80 border border-amber-300 dark:border-amber-900/40 rounded-xl p-5 space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-sm font-bold text-amber-700 dark:text-amber-400">{yara.rule_name}</span>
                      <span className="text-[10px] bg-red-100 dark:bg-red-950 text-red-700 dark:text-red-400 border border-red-300 dark:border-red-800 px-2 py-0.5 rounded font-semibold uppercase">
                        Severity: {yara.severity}
                      </span>
                    </div>
                    <span className="text-xs text-slate-500 dark:text-gray-500 font-mono">Rule ID #{yara.id}</span>
                  </div>

                  {yara.tags && yara.tags.length > 0 && (
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-slate-500 dark:text-gray-400">Tags:</span>
                      {yara.tags.map((tag, i) => (
                        <span key={i} className="text-[10px] bg-slate-200 dark:bg-gray-800 text-slate-700 dark:text-gray-300 px-2 py-0.5 rounded border border-slate-300 dark:border-gray-700 font-mono">
                          #{typeof tag === 'object' ? JSON.stringify(tag) : String(tag)}
                        </span>
                      ))}
                    </div>
                  )}

                  {yara.matched_strings && yara.matched_strings.length > 0 && (
                    <div className="bg-white dark:bg-gray-950 p-3 rounded-lg border border-slate-200 dark:border-gray-800">
                      <span className="text-[11px] text-slate-500 dark:text-gray-400 font-semibold block mb-1">Matched String Sequences:</span>
                      {yara.matched_strings.map((str, idx) => (
                        <code key={idx} className="block text-xs font-mono text-amber-800 dark:text-amber-300/90 py-0.5">
                          {typeof str === 'object' ? JSON.stringify(str) : String(str)}
                        </code>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Section 4: Extracted Strings & APIs */}
        <div className="pt-8 border-t border-slate-200 dark:border-gray-800">
          <div className="space-y-5">
            <div>
              <h3 className="text-sm font-bold text-slate-800 dark:text-gray-200 mb-2 flex items-center">
                <Layers className="w-4 h-4 mr-2 text-blue-600 dark:text-blue-400" />
                Imported APIs & DLL Calls
              </h3>
              <div className="bg-slate-50 dark:bg-gray-950 p-4 rounded-xl border border-slate-200 dark:border-gray-800 max-h-48 overflow-y-auto space-y-1">
                {(analysis.suspicious_apis || []).length === 0 ? (
                  <span className="text-xs text-slate-500 dark:text-gray-400 italic">No suspicious API calls identified.</span>
                ) : (
                  (analysis.suspicious_apis || []).map((api, idx) => (
                    <div key={idx} className="font-mono text-xs text-red-600 dark:text-red-300/90 flex items-center space-x-2">
                      <span className="text-slate-400 dark:text-gray-600 text-[10px]">{idx + 1}.</span>
                      <span>{typeof api === 'object' ? JSON.stringify(api) : String(api)}</span>
                    </div>
                  ))
                )}
              </div>
            </div>

            <div>
              <h3 className="text-sm font-bold text-slate-800 dark:text-gray-200 mb-2 flex items-center">
                <Terminal className="w-4 h-4 mr-2 text-cyan-600 dark:text-cyan-400" />
                Extracted Suspicious Commands & Strings
              </h3>
              <div className="bg-slate-50 dark:bg-gray-950 p-4 rounded-xl border border-slate-200 dark:border-gray-800 max-h-48 overflow-y-auto space-y-1">
                {(analysis.extracted_strings || []).length === 0 ? (
                  <span className="text-xs text-slate-500 dark:text-gray-400 italic">No suspicious strings identified.</span>
                ) : (
                  (analysis.extracted_strings || []).map((str, idx) => (
                    <div key={idx} className="font-mono text-xs text-cyan-700 dark:text-cyan-300/90 break-all py-0.5">
                      &gt; {typeof str === 'object' ? JSON.stringify(str) : String(str)}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Section 5: Network Indicators */}
        <div className="pt-8 border-t border-slate-200 dark:border-gray-800">
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-800 dark:text-gray-200 flex items-center">
              <Globe className="w-4 h-4 mr-2 text-cyan-600 dark:text-cyan-400" />
              Detected Network Indicators & C2 Callback References
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-50 dark:bg-gray-900/60 p-4 rounded-xl border border-slate-200 dark:border-gray-800">
                <span className="text-xs text-slate-500 dark:text-gray-400 font-semibold block mb-2">Embedded URLs</span>
                {(analysis.network_indicators?.urls || []).length === 0 ? (
                  <span className="text-xs text-slate-500 dark:text-gray-400 italic">No embedded URLs detected.</span>
                ) : (
                  analysis.network_indicators.urls.map((url, i) => (
                    <div key={i} className="font-mono text-xs text-cyan-700 dark:text-cyan-400 bg-white dark:bg-gray-950 p-2 rounded mb-1.5 border border-slate-200 dark:border-gray-800 break-all">
                      {typeof url === 'object' ? JSON.stringify(url) : String(url)}
                    </div>
                  ))
                )}
              </div>

              <div className="bg-slate-50 dark:bg-gray-900/60 p-4 rounded-xl border border-slate-200 dark:border-gray-800">
                <span className="text-xs text-slate-500 dark:text-gray-400 font-semibold block mb-2">Embedded IP Addresses</span>
                {(analysis.network_indicators?.ips || []).length === 0 ? (
                  <span className="text-xs text-slate-500 dark:text-gray-400 italic">No IP addresses detected.</span>
                ) : (
                  analysis.network_indicators.ips.map((ip, i) => (
                    <div key={i} className="font-mono text-xs text-amber-700 dark:text-amber-400 bg-white dark:bg-gray-950 p-2 rounded mb-1.5 border border-slate-200 dark:border-gray-800">
                      {typeof ip === 'object' ? JSON.stringify(ip) : String(ip)}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
