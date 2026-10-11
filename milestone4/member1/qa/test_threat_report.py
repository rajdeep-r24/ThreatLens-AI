import sys
from pathlib import Path

M3_PATH = (
    Path(__file__).resolve().parents[3]
    / "milestone3"
    / "member1"
    / "behavioral_analysis"
)

sys.path.insert(0, str(M3_PATH))

from threat_report import generate_threat_report


def test_threat_report_generation():

    threat_prediction = {
        "ml_prediction": "Malware",
        "ml_confidence": 0.98,
        "behavior_score": 78,
        "final_threat_score": 91,
        "threat_level": "Critical",
        "threat_category": "Potential Trojan / Process Injection Malware",
        "recommended_action": "Quarantine immediately and escalate",
        "detected_behaviors": [
            {
                "behavior": "Process Injection",
                "severity": "Critical",
                "confidence": 0.95,
                "evidence": [
                    "VirtualAllocEx",
                    "WriteProcessMemory"
                ],
                "description": "Process injection indicators detected."
            },
            {
                "behavior": "Persistence",
                "severity": "High",
                "confidence": 0.88,
                "evidence": [
                    r"CurrentVersion\Run"
                ],
                "description": "Persistence indicators detected."
            }
        ]
    }

    report = generate_threat_report(
        filename="qa_test_sample.exe",
        sha256_hash="a" * 64,
        threat_prediction=threat_prediction
    )

    assert isinstance(report, dict)

    assert "report_metadata" in report
    assert "file_information" in report
    assert "ml_analysis" in report
    assert "behavioral_analysis" in report
    assert "threat_assessment" in report
    assert "response" in report
    assert "security_summary" in report

    assert report["file_information"]["filename"] == "qa_test_sample.exe"

    assert report["ml_analysis"]["prediction"] == "Malware"
    assert report["ml_analysis"]["confidence"] == 0.98

    assert report["behavioral_analysis"]["behavior_count"] == 2
    assert report["behavioral_analysis"]["behavior_score"] == 78

    assert report["threat_assessment"]["final_threat_score"] == 91
    assert report["threat_assessment"]["threat_level"] == "Critical"

    assert (
        report["response"]["recommended_action"]
        == "Quarantine immediately and escalate"
    )


def test_benign_report_generation():

    threat_prediction = {
        "ml_prediction": "Benign",
        "ml_confidence": 0.99,
        "behavior_score": 0,
        "final_threat_score": 0,
        "threat_level": "Low",
        "threat_category": "Benign",
        "recommended_action": "Allow with monitoring",
        "detected_behaviors": []
    }

    report = generate_threat_report(
        filename="qa_benign.exe",
        sha256_hash="b" * 64,
        threat_prediction=threat_prediction
    )

    assert isinstance(report, dict)

    assert report["file_information"]["filename"] == "qa_benign.exe"
    assert report["ml_analysis"]["prediction"] == "Benign"
    assert report["behavioral_analysis"]["behavior_count"] == 0
    assert report["behavioral_analysis"]["behavior_score"] == 0
    assert report["threat_assessment"]["threat_level"] == "Low"
    assert report["threat_assessment"]["final_threat_score"] == 0
    assert (
        report["response"]["recommended_action"]
        == "Allow with monitoring"
    )