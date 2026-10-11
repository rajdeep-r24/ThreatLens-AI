import sys
from pathlib import Path

M3_PATH = (
    Path(__file__).resolve().parents[3]
    / "milestone3"
    / "member1"
    / "behavioral_analysis"
)

sys.path.insert(0, str(M3_PATH))

from behavioral_analysis import analyze_behavior
from threat_prediction import predict_threat


def test_empty_behavioral_input():

    result = analyze_behavior(
        suspicious_apis=[],
        extracted_strings=[],
        network_indicators={},
        pe_headers={},
        yara_results=[]
    )

    assert isinstance(result, dict)
    assert result["behavior_count"] == 0
    assert result["behavior_score"] == 0


def test_multiple_behavior_indicators():

    result = analyze_behavior(
        suspicious_apis=[
            "VirtualAllocEx",
            "WriteProcessMemory",
            "CreateRemoteThread",
            "CreateProcess"
        ],
        extracted_strings=[
            "powershell.exe",
            "Invoke-Expression",
            r"CurrentVersion\Run"
        ],
        network_indicators={
            "urls": [
                "https://example.com/payload.exe"
            ]
        },
        pe_headers={},
        yara_results=[]
    )

    assert isinstance(result, dict)
    assert result["behavior_count"] >= 3
    assert result["behavior_score"] > 0
    assert result["behavior_score"] <= 100


def test_low_confidence_benign_prediction():

    behavioral_result = {
        "behaviors": [],
        "behavior_count": 0,
        "behavior_score": 0,
        "threat_category": "No Significant Behavioral Threat Detected",
        "summary": "No significant behavioral indicators detected."
    }

    result = predict_threat(
        "Benign",
        0.50,
        behavioral_result
    )

    assert isinstance(result, dict)
    assert 0 <= result["final_threat_score"] <= 100
    assert result["threat_level"] in [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]


def test_behavior_score_never_exceeds_100():

    result = analyze_behavior(
        suspicious_apis=[
            "VirtualAlloc",
            "VirtualAllocEx",
            "WriteProcessMemory",
            "CreateRemoteThread",
            "NtWriteVirtualMemory",
            "NtCreateThreadEx",
            "QueueUserAPC",
            "CreateProcess",
            "WinExec",
            "ShellExecute"
        ],
        extracted_strings=[
            "powershell.exe",
            "ExecutionPolicy Bypass",
            "-EncodedCommand",
            "Invoke-Expression",
            r"CurrentVersion\Run",
            r"CurrentVersion\RunOnce",
            "schtasks",
            "https://example.com/a.exe"
        ],
        network_indicators={
            "urls": [
                "https://example.com/a.exe",
                "https://example.com/b.exe"
            ]
        },
        pe_headers={},
        yara_results=[]
    )

    assert result["behavior_score"] <= 100