import time
import os
import sys
from typing import Dict, Any, List

# Ensure static_analysis module can be resolved from root
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from static_analysis.hashes import calculate_hashes
from static_analysis.file_info import get_file_info
from static_analysis.pe_analysis import analyze_pe
from static_analysis.strings import extract_strings
from static_analysis.indicators import extract_indicators

from backend.app.services.malware_detection import (
    extract_ml_features,
    predict_malware,
)
# Suspicious keywords & APIs common in malware
SUSPICIOUS_API_KEYWORDS = [
    "VirtualAlloc", "VirtualProtect", "WriteProcessMemory", "CreateRemoteThread",
    "OpenProcess", "AdjustTokenPrivileges", "RegSetValueEx", "URLDownloadToFile",
    "WinExec", "ShellExecute", "SetWindowsHookEx", "GetProcAddress", "LoadLibrary"
]

SUSPICIOUS_STRINGS = [
    "powershell", "cmd.exe", "wscript", "mimikatz", "sekurlsa", "lsass.exe",
    "reg add", "bypass", "hidden", "invoke-expression", "downloadstring"
]


def run_static_analysis_pipeline(file_path: str) -> Dict[str, Any]:
    """
    Execute the unified static analysis pipeline (Member 5 modules):
    1. Hashing (MD5, SHA-256)
    2. File Metadata (Size, Type, Name)
    3. PE Header & Section Analysis
    4. String & Indicator Extraction (URLs, IPs, Suspicious Commands)
    5. Heuristic Threat Scoring & Classification
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    start_time = time.time()

    # 1. Hashes
    hashes = calculate_hashes(file_path)

    # 2. File metadata
    info = get_file_info(file_path)

    # 3. PE Analysis
    pe_data = analyze_pe(file_path)

    # 4. String extraction
    all_strings = extract_strings(file_path, min_length=4)

    # 5. Network indicators
    indicators = extract_indicators(file_path)

    # 6. Suspicious API & String detection
    matched_suspicious_apis: List[str] = []
    if pe_data.get("is_pe") and "imports" in pe_data:
        for imp in pe_data["imports"]:
            dll = imp.get("dll", "")
            for func in imp.get("functions", []):
                for keyword in SUSPICIOUS_API_KEYWORDS:
                    if keyword.lower() in func.lower():
                        matched_suspicious_apis.append(f"{dll} -> {func}")

    matched_suspicious_strings = [
        s for s in all_strings
        if any(bad in s.lower() for bad in SUSPICIOUS_STRINGS)
    ][:20]  # Cap top 20 matches

    # 7. ML Malware Prediction
    ml_prediction = {"label": "N/A", "confidence": 0.0}
    if pe_data.get("is_pe"):
        try:
            ml_features = extract_ml_features(file_path)
            ml_prediction = predict_malware(ml_features)
        except Exception:
            pass

    # 8. Heuristic Risk Scoring (0 to 100)
    risk_score = 0
    threat_classification = "Benign Clean Document"
    recommended_action = "No Action Required"

    if pe_data.get("is_pe"):
        risk_score += 20  # Executable baseline

    if matched_suspicious_apis:
        risk_score += min(len(matched_suspicious_apis) * 15, 45)

    if matched_suspicious_strings:
        risk_score += min(len(matched_suspicious_strings) * 10, 30)

    if indicators.get("urls") or indicators.get("ip_addresses"):
        risk_score += 15

    risk_score = min(risk_score, 100)

    if risk_score >= 80:
        threat_classification = "High Risk Trojan / Malware"
        recommended_action = "Quarantine Immediately & Escalate to Security Analyst"
    elif risk_score >= 50:
        threat_classification = "Suspicious Binary / Potential Threat"
        recommended_action = "Perform Behavioral Dynamic Analysis"
    elif risk_score >= 25:
        threat_classification = "Low Risk Unclassified File"
        recommended_action = "Monitor File Activity"

    # 9. Combine ML prediction with heuristic risk score
    ml_confidence_percent = ml_prediction["confidence"] * 100

    if ml_prediction["label"] == "Malware":
        final_risk_score = max(
            risk_score,
            int(ml_confidence_percent)
        )
    else:
        final_risk_score = risk_score

    final_risk_score = min(final_risk_score, 100)

    scan_duration = round(time.time() - start_time, 2)

    return {
        "filename": info["file_name"],
        "file_size": info["file_size"],
        "file_type": info["file_type"],
        "md5_hash": hashes["md5"],
        "sha256_hash": hashes["sha256"],
        "pe_headers": pe_data if pe_data.get("is_pe") else None,
        "extracted_strings": matched_suspicious_strings or all_strings[:15],
        "suspicious_apis": matched_suspicious_apis,
        "network_indicators": indicators,
        "risk_score": risk_score,
        "threat_classification": threat_classification,
        "recommended_action": recommended_action,
        "ml_prediction": ml_prediction["label"],
        "ml_confidence": ml_prediction["confidence"],
        "final_risk_score": final_risk_score,
        "scan_duration": scan_duration
    }