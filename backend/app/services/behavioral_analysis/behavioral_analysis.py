"""
ThreatLens AI - Milestone 3
Member 1: AI Prediction & Behavioral Analysis

This module analyzes static malware indicators and identifies
potential malicious behaviors.

Important:
The detected behaviors represent static evidence associated with
a behavior. They do not prove that the behavior executed at runtime.
"""

from typing import Any, Dict, List


# ============================================================
# BEHAVIOR RULE DEFINITIONS
# ============================================================

PROCESS_INJECTION_APIS = {
    "virtualalloc",
    "virtualallocex",
    "writeprocessmemory",
    "createremotethread",
    "ntwritevirtualmemory",
    "ntcreatethreadex",
    "queueuserapc",
}

POWERSHELL_INDICATORS = {
    "powershell",
    "powershell.exe",
    "executionpolicy bypass",
    "-executionpolicy bypass",
    "-enc",
    "-encodedcommand",
    "invoke-expression",
    "iex ",
}

PERSISTENCE_INDICATORS = {
    "\\run",
    "\\runonce",
    "currentversion\\run",
    "currentversion\\runonce",
    "startup",
    "schtasks",
    "scheduled task",
    "service create",
}

PAYLOAD_DOWNLOAD_APIS = {
    "urldownloadtofile",
    "urldownloadtofilea",
    "urldownloadtofilew",
    "winhttpopen",
    "winhttpsendrequest",
    "internetopenurl",
    "urlmon.dll",
}

COMMAND_EXECUTION_INDICATORS = {
    "cmd.exe",
    "command.com",
    "shell_execute",
    "shellexecute",
    "createprocess",
    "winexec",
}

NETWORK_INDICATORS = {
    "http://",
    "https://",
    "ftp://",
    "socket",
    "connect",
    "internetopen",
    "wininet",
    "winhttp",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(value: Any) -> str:
    """Convert a value into normalized lowercase text."""
    if value is None:
        return ""

    return str(value).strip().lower()


def flatten_values(value: Any) -> List[str]:
    """
    Convert different indicator formats into a simple list of strings.

    Supports:
    - strings
    - lists
    - tuples
    - dictionaries
    - nested structures
    """

    results = []

    if value is None:
        return results

    if isinstance(value, str):
        results.append(value)
        return results

    if isinstance(value, dict):
        for key, item in value.items():
            results.extend(flatten_values(key))
            results.extend(flatten_values(item))
        return results

    if isinstance(value, (list, tuple, set)):
        for item in value:
            results.extend(flatten_values(item))
        return results

    results.append(str(value))

    return results


def contains_any(text: str, indicators) -> bool:
    """Check whether text contains any indicator."""
    normalized = normalize_text(text)

    return any(indicator in normalized for indicator in indicators)


def matching_indicators(values: List[str], indicators) -> List[str]:
    """
    Return the original values that match one or more indicators.
    """

    matches = []

    for value in values:
        normalized = normalize_text(value)

        for indicator in indicators:
            if indicator in normalized:
                matches.append(value)
                break

    return list(dict.fromkeys(matches))


# ============================================================
# BEHAVIOR DETECTION FUNCTIONS
# ============================================================

def detect_process_injection(suspicious_apis: List[str]) -> Dict[str, Any] | None:
    matches = matching_indicators(
        suspicious_apis,
        PROCESS_INJECTION_APIS
    )

    if not matches:
        return None

    # Multiple injection APIs provide stronger evidence.
    if len(matches) >= 3:
        severity = "Critical"
        confidence = 0.95
    elif len(matches) == 2:
        severity = "High"
        confidence = 0.90
    else:
        severity = "Medium"
        confidence = 0.75

    return {
        "behavior": "Process Injection",
        "severity": severity,
        "confidence": confidence,
        "evidence": matches,
        "description": (
            "APIs associated with memory manipulation and "
            "remote thread creation were detected."
        ),
    }


def detect_powershell(extracted_strings: List[str]) -> Dict[str, Any] | None:
    matches = matching_indicators(
        extracted_strings,
        POWERSHELL_INDICATORS
    )

    if not matches:
        return None

    severity = "High"
    confidence = 0.90 if len(matches) >= 2 else 0.80

    return {
        "behavior": "Suspicious PowerShell Execution",
        "severity": severity,
        "confidence": confidence,
        "evidence": matches,
        "description": (
            "PowerShell-related commands or execution indicators "
            "were found in extracted strings."
        ),
    }


def detect_persistence(extracted_strings: List[str]) -> Dict[str, Any] | None:
    matches = matching_indicators(
        extracted_strings,
        PERSISTENCE_INDICATORS
    )

    if not matches:
        return None

    return {
        "behavior": "Persistence",
        "severity": "High",
        "confidence": 0.88,
        "evidence": matches,
        "description": (
            "Registry, startup, scheduled-task, or service "
            "persistence indicators were detected."
        ),
    }


def detect_payload_download(
    suspicious_apis: List[str],
    network_indicators: Any
) -> Dict[str, Any] | None:

    api_matches = matching_indicators(
        suspicious_apis,
        PAYLOAD_DOWNLOAD_APIS
    )

    network_values = flatten_values(network_indicators)

    network_matches = []

    for value in network_values:
        normalized = normalize_text(value)

        if any(
            indicator in normalized
            for indicator in ["http://", "https://", "ftp://"]
        ):
            network_matches.append(value)

    evidence = list(dict.fromkeys(api_matches + network_matches))

    if not evidence:
        return None

    if api_matches and network_matches:
        severity = "High"
        confidence = 0.92
    else:
        severity = "Medium"
        confidence = 0.78

    return {
        "behavior": "Payload Download / Network Retrieval",
        "severity": severity,
        "confidence": confidence,
        "evidence": evidence,
        "description": (
            "Network retrieval APIs or remote resource indicators "
            "were detected."
        ),
    }


def detect_command_execution(
    extracted_strings: List[str],
    suspicious_apis: List[str]
) -> Dict[str, Any] | None:

    string_matches = matching_indicators(
        extracted_strings,
        COMMAND_EXECUTION_INDICATORS
    )

    api_matches = matching_indicators(
        suspicious_apis,
        COMMAND_EXECUTION_INDICATORS
    )

    evidence = list(dict.fromkeys(string_matches + api_matches))

    if not evidence:
        return None

    return {
        "behavior": "Command Execution",
        "severity": "Medium",
        "confidence": 0.80,
        "evidence": evidence,
        "description": (
            "Command shell or process execution indicators "
            "were detected."
        ),
    }


def detect_network_communication(
    suspicious_apis: List[str],
    network_indicators: Any
) -> Dict[str, Any] | None:

    network_values = flatten_values(network_indicators)

    network_matches = []

    for value in network_values:
        normalized = normalize_text(value)

        if any(
            indicator in normalized
            for indicator in NETWORK_INDICATORS
        ):
            network_matches.append(value)

    api_matches = matching_indicators(
        suspicious_apis,
        NETWORK_INDICATORS
    )

    evidence = list(dict.fromkeys(network_matches + api_matches))

    if not evidence:
        return None

    return {
        "behavior": "Network Communication",
        "severity": "Medium",
        "confidence": 0.75,
        "evidence": evidence,
        "description": (
            "Network communication indicators were detected."
        ),
    }


def detect_yara_behavior(yara_results: Any) -> Dict[str, Any] | None:
    """
    Analyze YARA matches.

    YARA detection itself is treated as supporting evidence,
    not as proof of a specific runtime behavior.
    """

    if not yara_results:
        return None

    matches = []

    for result in yara_results:
        if isinstance(result, dict):
            rule_name = result.get("rule_name", "Unknown YARA rule")
            severity = normalize_text(result.get("severity", "medium"))

            matches.append({
                "rule_name": rule_name,
                "severity": severity,
            })

        else:
            matches.append({
                "rule_name": str(result),
                "severity": "medium",
            })

    high_or_critical = any(
        item["severity"] in {"high", "critical"}
        for item in matches
    )

    severity = "High" if high_or_critical else "Medium"
    confidence = 0.90 if high_or_critical else 0.75

    return {
        "behavior": "YARA Rule Detection",
        "severity": severity,
        "confidence": confidence,
        "evidence": matches,
        "description": (
            "One or more YARA rules matched the analyzed file."
        ),
    }


# ============================================================
# SCORING
# ============================================================

SEVERITY_SCORES = {
    "Low": 10,
    "Medium": 20,
    "High": 30,
    "Critical": 40,
}


def calculate_behavior_score(behaviors: List[Dict[str, Any]]) -> int:
    """
    Calculate a normalized behavioral risk score from 0 to 100.
    """

    if not behaviors:
        return 0

    raw_score = 0

    for behavior in behaviors:
        severity = behavior.get("severity", "Low")
        confidence = float(behavior.get("confidence", 0))

        severity_score = SEVERITY_SCORES.get(severity, 10)

        raw_score += severity_score * confidence

    return min(round(raw_score), 100)


def classify_threat(
    behaviors: List[Dict[str, Any]],
    behavior_score: int
) -> str:

    if not behaviors:
        return "No Significant Behavioral Threat Detected"

    behavior_names = {
        behavior["behavior"]
        for behavior in behaviors
    }

    if "Process Injection" in behavior_names:
        if behavior_score >= 70:
            return "High-Risk Trojan / Malware"
        return "Potential Process Injection Malware"

    if behavior_score >= 70:
        return "High-Risk Malware"

    if behavior_score >= 40:
        return "Suspicious / Potentially Malicious"

    return "Low-Risk Suspicious Activity"


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def analyze_behavior(
    suspicious_apis=None,
    extracted_strings=None,
    network_indicators=None,
    pe_headers=None,
    yara_results=None,
) -> Dict[str, Any]:
    """
    Main behavioral-analysis function.

    Parameters:
        suspicious_apis:
            APIs extracted during static analysis.

        extracted_strings:
            Strings extracted from the analyzed file.

        network_indicators:
            URLs, IP addresses, domains, or network-related evidence.

        pe_headers:
            PE header information. Reserved for additional
            behavioral rules in later stages.

        yara_results:
            YARA rule matches and severities.

    Returns:
        Structured behavioral analysis result.
    """

    suspicious_apis = flatten_values(suspicious_apis)
    extracted_strings = flatten_values(extracted_strings)

    behaviors = []

    detectors = [
        detect_process_injection(suspicious_apis),
        detect_powershell(extracted_strings),
        detect_persistence(extracted_strings),
        detect_payload_download(
            suspicious_apis,
            network_indicators
        ),
        detect_command_execution(
            extracted_strings,
            suspicious_apis
        ),
        detect_network_communication(
            suspicious_apis,
            network_indicators
        ),
        detect_yara_behavior(yara_results),
    ]

    for result in detectors:
        if result is not None:
            behaviors.append(result)

    behavior_score = calculate_behavior_score(behaviors)

    threat_category = classify_threat(
        behaviors,
        behavior_score
    )

    if behaviors:
        behavior_names = [
            behavior["behavior"]
            for behavior in behaviors
        ]

        summary = (
            "Detected behavioral indicators: "
            + ", ".join(behavior_names)
            + "."
        )
    else:
        summary = "No significant behavioral indicators detected."

    return {
        "behaviors": behaviors,
        "behavior_count": len(behaviors),
        "behavior_score": behavior_score,
        "threat_category": threat_category,
        "summary": summary,
    }


# ============================================================
# SIMPLE MANUAL TEST
# ============================================================

if __name__ == "__main__":

    sample_result = analyze_behavior(
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
            ],
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

    import json

    print(
        json.dumps(
            sample_result,
            indent=4
        )
    )