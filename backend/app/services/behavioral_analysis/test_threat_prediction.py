import json

from behavioral_analysis import analyze_behavior
from threat_prediction import predict_threat


def run_test(name, ml_prediction, ml_confidence, behavioral_result):
    result = predict_threat(
        ml_prediction=ml_prediction,
        ml_confidence=ml_confidence,
        behavioral_result=behavioral_result,
    )

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print(json.dumps(result, indent=4))

    print("\nFinal threat score:", result["final_threat_score"])
    print("Threat level:", result["threat_level"])
    print("Threat category:", result["threat_category"])
    print("Recommended action:", result["recommended_action"])


# ============================================================
# TEST 1 — BENIGN ML + NO BEHAVIOR
# ============================================================

behavior = analyze_behavior(
    suspicious_apis=[],
    extracted_strings=[],
    network_indicators={},
    pe_headers={},
    yara_results=[]
)

run_test(
    "TEST 1 - BENIGN FILE",
    "Benign",
    0.99,
    behavior
)


# ============================================================
# TEST 2 — BENIGN ML + SUSPICIOUS BEHAVIOR
# ============================================================

behavior = analyze_behavior(
    suspicious_apis=[],
    extracted_strings=[
        "powershell.exe -ExecutionPolicy Bypass"
    ],
    network_indicators={},
    pe_headers={},
    yara_results=[]
)

run_test(
    "TEST 2 - BENIGN ML + POWERSHELL INDICATOR",
    "Benign",
    0.80,
    behavior
)


# ============================================================
# TEST 3 — MALWARE ML + NO BEHAVIOR
# ============================================================

behavior = analyze_behavior(
    suspicious_apis=[],
    extracted_strings=[],
    network_indicators={},
    pe_headers={},
    yara_results=[]
)

run_test(
    "TEST 3 - MALWARE ML + NO BEHAVIOR",
    "Malware",
    0.95,
    behavior
)


# ============================================================
# TEST 4 — MALWARE ML + PROCESS INJECTION
# ============================================================

behavior = analyze_behavior(
    suspicious_apis=[
        "Kernel32.dll -> VirtualAlloc",
        "Kernel32.dll -> WriteProcessMemory",
        "Kernel32.dll -> CreateRemoteThread"
    ],
    extracted_strings=[],
    network_indicators={},
    pe_headers={},
    yara_results=[]
)

run_test(
    "TEST 4 - MALWARE ML + PROCESS INJECTION",
    "Malware",
    0.95,
    behavior
)


# ============================================================
# TEST 5 — MALWARE ML + MULTIPLE BEHAVIORS
# ============================================================

behavior = analyze_behavior(
    suspicious_apis=[
        "Kernel32.dll -> VirtualAlloc",
        "Kernel32.dll -> WriteProcessMemory",
        "Kernel32.dll -> CreateRemoteThread",
        "Urlmon.dll -> URLDownloadToFileA"
    ],
    extracted_strings=[
        "powershell.exe -ExecutionPolicy Bypass -W Hidden",
        "cmd.exe /c reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    ],
    network_indicators={
        "urls": [
            "http://malicious-site.com/payload.ps1"
        ]
    },
    pe_headers={},
    yara_results=[
        {
            "rule_name": "Suspicious_PowerShell_Execution",
            "severity": "high"
        }
    ]
)

run_test(
    "TEST 5 - MALWARE ML + MULTIPLE BEHAVIORS",
    "Malware",
    0.948,
    behavior
)