import json

from behavioral_analysis import analyze_behavior


def run_test(name, result):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print(json.dumps(result, indent=4))

    print(f"\nBehavior count : {result['behavior_count']}")
    print(f"Behavior score : {result['behavior_score']}")
    print(f"Threat category: {result['threat_category']}")


# ============================================================
# TEST 1 — BENIGN / NO SUSPICIOUS INDICATORS
# ============================================================

benign_result = analyze_behavior(
    suspicious_apis=[],
    extracted_strings=[
        "Hello World",
        "Application started successfully",
        "Configuration loaded"
    ],
    network_indicators={},
    pe_headers={},
    yara_results=[]
)

run_test(
    "TEST 1 - BENIGN FILE",
    benign_result
)


# ============================================================
# TEST 2 — POWERSHELL ONLY
# ============================================================

powershell_result = analyze_behavior(
    suspicious_apis=[],
    extracted_strings=[
        "powershell.exe -ExecutionPolicy Bypass"
    ],
    network_indicators={},
    pe_headers={},
    yara_results=[]
)

run_test(
    "TEST 2 - POWERSHELL ACTIVITY",
    powershell_result
)


# ============================================================
# TEST 3 — PERSISTENCE
# ============================================================

persistence_result = analyze_behavior(
    suspicious_apis=[],
    extracted_strings=[
        "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    ],
    network_indicators={},
    pe_headers={},
    yara_results=[]
)

run_test(
    "TEST 3 - PERSISTENCE",
    persistence_result
)


# ============================================================
# TEST 4 — PROCESS INJECTION
# ============================================================

injection_result = analyze_behavior(
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
    "TEST 4 - PROCESS INJECTION",
    injection_result
)


# ============================================================
# TEST 5 — NETWORK / PAYLOAD DOWNLOAD
# ============================================================

network_result = analyze_behavior(
    suspicious_apis=[
        "Urlmon.dll -> URLDownloadToFileA"
    ],
    extracted_strings=[],
    network_indicators={
        "urls": [
            "http://example.com/payload.exe"
        ]
    },
    pe_headers={},
    yara_results=[]
)

run_test(
    "TEST 5 - PAYLOAD DOWNLOAD",
    network_result
)


# ============================================================
# TEST 6 — MULTIPLE HIGH-RISK BEHAVIORS
# ============================================================

malware_result = analyze_behavior(
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
        ],
        "ips": [
            "185.220.101.5"
        ]
    },
    pe_headers={
        "entry_point": "0x00401000",
        "number_of_sections": 5
    },
    yara_results=[
        {
            "rule_name": "Suspicious_PowerShell_Execution",
            "severity": "high"
        }
    ]
)

run_test(
    "TEST 6 - MULTIPLE MALICIOUS BEHAVIORS",
    malware_result
)