import sys
from pathlib import Path

# Add Milestone 3 behavioral analysis folder to Python path
M3_PATH = Path(__file__).resolve().parents[3] / "milestone3" / "member1" / "behavioral_analysis"
sys.path.insert(0, str(M3_PATH))

from behavioral_analysis import analyze_behavior


def test_benign_input():
    result = analyze_behavior(
        suspicious_apis=[],
        extracted_strings=[],
        network_indicators={},
        pe_headers={},
        yara_results=[]
    )

    assert result["behavior_count"] == 0
    assert result["behavior_score"] == 0
    assert result["threat_category"] == "No Significant Behavioral Threat Detected"


def test_powershell_detection():
    result = analyze_behavior(
        suspicious_apis=[],
        extracted_strings=["powershell.exe", "Invoke-Expression"],
        network_indicators={},
        pe_headers={},
        yara_results=[]
    )

    assert result["behavior_count"] >= 1
    assert any(
        behavior["behavior"] == "Suspicious PowerShell Execution"
        for behavior in result["behaviors"]
    )

    assert result["behavior_count"] >= 1
    assert any(
        behavior["behavior"] == "Suspicious PowerShell Execution"
        for behavior in result["behaviors"]
    )


def test_persistence_detection():
    result = analyze_behavior(
        suspicious_apis=[],
        extracted_strings=[r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"],
        network_indicators={},
        pe_headers={},
        yara_results=[]
    )

    assert result["behavior_count"] >= 1
    assert any(
        behavior["behavior"] == "Persistence"
        for behavior in result["behaviors"]
    )


def test_process_injection_detection():
    result = analyze_behavior(
        suspicious_apis=[
            "VirtualAllocEx",
            "WriteProcessMemory",
            "CreateRemoteThread"
        ],
        extracted_strings=[],
        network_indicators={},
        pe_headers={},
        yara_results=[]
    )

    assert result["behavior_count"] >= 1
    assert any(
        behavior["behavior"] == "Process Injection"
        for behavior in result["behaviors"]
    )


def test_payload_download_detection():
    result = analyze_behavior(
        suspicious_apis=["URLDownloadToFileA"],
        extracted_strings=["https://malicious.example/payload.exe"],
        network_indicators={
            "urls": ["https://malicious.example/payload.exe"]
        },
        pe_headers={},
        yara_results=[]
    )

    assert result["behavior_count"] >= 1
    assert any(
        behavior["behavior"] == "Payload Download / Network Retrieval"
        for behavior in result["behaviors"]
    )


def test_multiple_malicious_behaviors():
    result = analyze_behavior(
        suspicious_apis=[
            "VirtualAllocEx",
            "WriteProcessMemory",
            "CreateRemoteThread",
            "powershell.exe",
            "Invoke-Expression",
            "URLDownloadToFileA",
            "CreateProcess"
        ],
        extracted_strings=[
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
            "https://malicious.example/payload.exe"
        ],
        network_indicators={
            "urls": ["https://malicious.example/payload.exe"]
        },
        pe_headers={},
        yara_results=["malware_rule"]
    )

    assert result["behavior_count"] >= 4
    assert result["behavior_score"] > 0
    assert result["threat_category"] != "No Significant Behavioral Threat Detected"