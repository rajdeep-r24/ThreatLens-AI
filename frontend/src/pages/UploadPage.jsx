import React, { useState } from 'react';
import { UploadCloud, File, CheckCircle2, Shield, AlertCircle, ArrowRight, RefreshCw } from 'lucide-react';

export default function UploadPage({ onUploadComplete }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUploadSubmit = () => {
    if (!selectedFile) return;
    setUploading(true);
    setProgress(15);

    // Simulate analysis pipeline progress: upload -> hash calculation -> static analysis -> YARA scan
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setUploading(false);
          // Trigger redirect to detailed analysis result
          onUploadComplete(1); // Navigates to sample static report for invoice.exe
          return 100;
        }
        return prev + 25;
      });
    }, 400);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-white">Suspicious File Scanner & Analysis</h1>
        <p className="text-sm text-gray-400 max-w-xl mx-auto">
          Upload binary executables (.exe, .dll), documents, or raw samples for static analysis, hash calculation, PE header extraction, and YARA signature matching.
        </p>
      </div>

      {/* Upload Box */}
      <div
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-2xl p-10 text-center transition-all bg-[#111827] ${
          dragActive
            ? 'border-blue-500 bg-blue-950/20 cyber-glow-blue'
            : selectedFile
            ? 'border-emerald-500/60 bg-emerald-950/10'
            : 'border-gray-800 hover:border-gray-700'
        }`}
      >
        {!selectedFile ? (
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 bg-blue-600/10 border border-blue-500/30 rounded-2xl flex items-center justify-center text-blue-400">
              <UploadCloud className="w-8 h-8" />
            </div>
            <div>
              <p className="text-base font-semibold text-white">
                Drag and drop your file here, or{' '}
                <label className="text-blue-400 hover:underline cursor-pointer">
                  browse files
                  <input
                    type="file"
                    onChange={handleFileChange}
                    className="hidden"
                    accept=".exe,.dll,.pdf,.doc,.docx,.bin,.sys"
                  />
                </label>
              </p>
              <p className="text-xs text-gray-400 mt-1">
                Supports PE Executables, DLLs, PDFs, Scripts (Max file size: 50MB)
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 bg-emerald-600/10 border border-emerald-500/30 rounded-2xl flex items-center justify-center text-emerald-400">
              <File className="w-8 h-8" />
            </div>

            <div>
              <h3 className="text-lg font-bold text-white">{selectedFile.name}</h3>
              <p className="text-xs text-gray-400 font-mono mt-0.5">
                {(selectedFile.size / 1024).toFixed(1)} KB • {selectedFile.type || 'Binary Stream'}
              </p>
            </div>

            {!uploading ? (
              <div className="flex justify-center space-x-3 pt-2">
                <button
                  onClick={() => setSelectedFile(null)}
                  className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs font-medium rounded-xl border border-gray-700 transition-colors"
                >
                  Change File
                </button>
                <button
                  onClick={handleUploadSubmit}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-xl shadow-lg hover:shadow-blue-500/20 transition-all flex items-center space-x-2"
                >
                  <span>Start Static Analysis Scan</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="max-w-md mx-auto space-y-3 pt-2">
                <div className="flex items-center justify-between text-xs text-gray-300">
                  <span className="flex items-center">
                    <RefreshCw className="w-3.5 h-3.5 mr-1.5 animate-spin text-blue-400" />
                    Executing Static Pipeline & YARA Engines...
                  </span>
                  <span className="font-mono font-bold text-blue-400">{progress}%</span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-2.5 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-cyan-400 h-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Info Callouts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 space-y-2">
          <div className="text-blue-400 font-semibold text-sm flex items-center">
            <Shield className="w-4 h-4 mr-1.5" />
            Static Safe Analysis
          </div>
          <p className="text-xs text-gray-400">
            Files are inspected statically without execution in isolated sandboxed storage.
          </p>
        </div>

        <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 space-y-2">
          <div className="text-amber-400 font-semibold text-sm flex items-center">
            <AlertCircle className="w-4 h-4 mr-1.5" />
            YARA Signature Matching
          </div>
          <p className="text-xs text-gray-400">
            Matches binary sequences against signature rule sets to identify malware families.
          </p>
        </div>

        <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 space-y-2">
          <div className="text-emerald-400 font-semibold text-sm flex items-center">
            <CheckCircle2 className="w-4 h-4 mr-1.5" />
            Automated Risk Scoring
          </div>
          <p className="text-xs text-gray-400">
            Generates normalized 0-100 risk score and actionable analyst recommendations.
          </p>
        </div>
      </div>
    </div>
  );
}
