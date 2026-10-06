import sys
from pathlib import Path

M3_PATH = (
    Path(__file__).resolve().parents[3]
    / "milestone3"
    / "member1"
    / "behavioral_analysis"
)

sys.path.insert(0, str(M3_PATH))

from threat_prediction import predict_threat


def test_benign_no_behavior():
    result = predict_threat(
        ml_prediction="Benign",
        ml_confidence=1.0,
        behavioral_result={
            "behaviors": [],
            "behavior_count": 0,
            "behavior_score": 0,
            "threat_category": "No Significant Behavioral Threat Detected"
        }
    )

    assert result["threat_level"] == "Low"
    assert result["threat_category"] == "Benign"
    assert result["recommended_action"] == "Allow with monitoring"


def test_benign_powershell():
    result = predict_threat(
        ml_prediction="Benign",
        ml_confidence=1.0,
        behavioral_result={
            "behaviors": [
                {
                    "behavior": "Suspicious PowerShell Execution",
                    "severity": "High",
                    "confidence": 0.8
                }
            ],
            "behavior_count": 1,
            "behavior_score": 24,
            "threat_category": "Suspicious / Potentially Malicious"
        }
    )

    assert result["threat_level"] == "Medium"
    assert result["recommended_action"] == "Flag for security review"


def test_malware_no_behavior():
    result = predict_threat(
        ml_prediction="Malware",
        ml_confidence=1.0,
        behavioral_result={
            "behaviors": [],
            "behavior_count": 0,
            "behavior_score": 0,
            "threat_category": "No Significant Behavioral Threat Detected"
        }
    )

    assert result["threat_level"] == "Medium"
    assert result["threat_category"] == "Potential Malware"


def test_malware_process_injection():
    result = predict_threat(
        ml_prediction="Malware",
        ml_confidence=1.0,
        behavioral_result={
            "behaviors": [
                {
                    "behavior": "Process Injection",
                    "severity": "Critical",
                    "confidence": 0.95
                }
            ],
            "behavior_count": 1,
            "behavior_score": 38,
            "threat_category": "Potential Process Injection Malware"
        }
    )

    assert result["threat_level"] == "Critical"
    assert "Process Injection" in result["threat_category"]
    assert result["recommended_action"] == "Quarantine immediately and escalate"


def test_malware_multiple_behaviors():
    result = predict_threat(
        ml_prediction="Malware",
        ml_confidence=1.0,
        behavioral_result={
            "behaviors": [
                {
                    "behavior": "Process Injection",
                    "severity": "Critical",
                    "confidence": 0.95
                },
                {
                    "behavior": "Persistence",
                    "severity": "High",
                    "confidence": 0.88
                },
                {
                    "behavior": "Suspicious PowerShell Execution",
                    "severity": "High",
                    "confidence": 0.8
                }
            ],
            "behavior_count": 3,
            "behavior_score": 85,
            "threat_category": "High-Risk Trojan / Malware"
        }
    )

    assert result["threat_level"] == "Critical"
    assert result["final_threat_score"] >= 70
    assert result["recommended_action"] == "Quarantine immediately and escalate"