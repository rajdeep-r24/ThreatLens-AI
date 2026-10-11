"""
ThreatLens AI - Milestone 3
Member 1: Threat Prediction Engine

Combines:
1. Milestone 2 ML malware prediction
2. ML confidence
3. Behavioral analysis score
4. Detected behavioral evidence

This module does not retrain the ML model.
It combines existing ML output with behavioral intelligence.
"""


from typing import Any, Dict, List


# ============================================================
# THREAT LEVEL THRESHOLDS
# ============================================================

THREAT_LEVELS = {
    "LOW": "Low",
    "MEDIUM": "Medium",
    "HIGH": "High",
    "CRITICAL": "Critical",
}


# ============================================================
# FINAL THREAT SCORE
# ============================================================

def calculate_threat_score(
    ml_prediction: str,
    ml_confidence: float,
    behavior_score: int,
) -> int:
    """
    Combine ML confidence and behavioral evidence.

    ML contributes up to 60 points.
    Behavioral analysis contributes up to 40 points.

    Total = 0 to 100.
    """

    ml_prediction = str(ml_prediction).strip().lower()

    ml_confidence = max(
        0.0,
        min(float(ml_confidence), 1.0)
    )

    behavior_score = max(
        0,
        min(int(behavior_score), 100)
    )

    # Malware prediction contributes to threat score.
    if ml_prediction == "malware":
        ml_score = ml_confidence * 60
    else:
        # A benign ML prediction should contribute very little.
        ml_score = (1 - ml_confidence) * 20

    behavioral_contribution = behavior_score * 0.40

    final_score = ml_score + behavioral_contribution

    return min(round(final_score), 100)


# ============================================================
# THREAT LEVEL
# ============================================================

def determine_threat_level(
    final_score: int,
    behaviors: List[Dict[str, Any]]
) -> str:

    if not behaviors:
        if final_score >= 70:
            return THREAT_LEVELS["HIGH"]

        if final_score >= 40:
            return THREAT_LEVELS["MEDIUM"]

        return THREAT_LEVELS["LOW"]

    has_critical_behavior = any(
        behavior.get("severity") == "Critical"
        for behavior in behaviors
    )

    has_high_behavior = any(
        behavior.get("severity") == "High"
        for behavior in behaviors
    )

    # Critical behavior combined with a strong overall score
    # should be treated as a critical threat.
    if has_critical_behavior and final_score >= 60:
        return THREAT_LEVELS["CRITICAL"]

    # Multiple suspicious behaviors increase the threat level.
    if has_critical_behavior:
        return THREAT_LEVELS["HIGH"]

    if has_high_behavior and final_score >= 40:
        return THREAT_LEVELS["HIGH"]

    if has_high_behavior:
        return THREAT_LEVELS["MEDIUM"]

    if final_score >= 40:
        return THREAT_LEVELS["MEDIUM"]

    return THREAT_LEVELS["LOW"]

# ============================================================
# THREAT CATEGORY
# ============================================================

def determine_threat_category(
    ml_prediction: str,
    behaviors: List[Dict[str, Any]]
) -> str:

    ml_prediction = str(ml_prediction).strip().lower()

    behavior_names = {
        behavior.get("behavior")
        for behavior in behaviors
    }

    if "Process Injection" in behavior_names:
        return "Potential Trojan / Process Injection Malware"

    if "Persistence" in behavior_names:
        return "Potential Persistence-Based Malware"

    if "Suspicious PowerShell Execution" in behavior_names:
        return "Potential PowerShell-Based Threat"

    if "Payload Download / Network Retrieval" in behavior_names:
        return "Potential Downloader / Network-Based Threat"

    if ml_prediction == "malware":
        return "Potential Malware"

    if behaviors:
        return "Suspicious Activity"

    return "Benign"


# ============================================================
# RECOMMENDED ACTION
# ============================================================

def recommend_action(
    threat_level: str
) -> str:

    actions = {
        "Low": "Allow with monitoring",
        "Medium": "Flag for security review",
        "High": "Quarantine and investigate",
        "Critical": "Quarantine immediately and escalate",
    }

    return actions.get(
        threat_level,
        "Review manually"
    )

# ============================================================
# MAIN THREAT PREDICTION FUNCTION
# ============================================================

def predict_threat(
    ml_prediction: str,
    ml_confidence: float,
    behavioral_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate a final threat prediction by combining
    ML classification with behavioral analysis.
    """

    behaviors = behavioral_result.get(
        "behaviors",
        []
    )

    behavior_score = behavioral_result.get(
        "behavior_score",
        0
    )

    final_score = calculate_threat_score(
        ml_prediction=ml_prediction,
        ml_confidence=ml_confidence,
        behavior_score=behavior_score,
    )

    threat_level = determine_threat_level(
        final_score,
        behaviors
    )

    threat_category = determine_threat_category(
        ml_prediction,
        behaviors
    )

    recommended_action = recommend_action(
        threat_level
    )

    return {
        "ml_prediction": ml_prediction,
        "ml_confidence": round(
            float(ml_confidence),
            4
        ),
        "behavior_score": behavior_score,
        "final_threat_score": final_score,
        "threat_level": threat_level,
        "threat_category": threat_category,
        "detected_behaviors": behaviors,
        "recommended_action": recommended_action,
    }


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    from behavioral_analysis import analyze_behavior

    behavioral_result = analyze_behavior(
        suspicious_apis=[
            "Kernel32.dll -> VirtualAlloc",
            "Kernel32.dll -> WriteProcessMemory",
            "Kernel32.dll -> CreateRemoteThread",
            "Urlmon.dll -> URLDownloadToFileA",
        ],
        extracted_strings=[
            "powershell.exe -ExecutionPolicy Bypass -W Hidden",
            "cmd.exe /c reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        ],
        network_indicators={
            "urls": [
                "http://malicious-site.com/payload.ps1"
            ],
            "ips": [
                "185.220.101.5"
            ]
        },
        pe_headers={
            "entry_point": "0x00401000",
            "number_of_sections": 5,
        },
        yara_results=[
            {
                "rule_name": "Suspicious_PowerShell_Execution",
                "severity": "high",
            }
        ],
    )

    result = predict_threat(
        ml_prediction="Malware",
        ml_confidence=0.948,
        behavioral_result=behavioral_result,
    )

    import json

    print(
        json.dumps(
            result,
            indent=4
        )
    )