from behavioral_analysis import analyze_behavior
from threat_prediction import predict_threat


# =========================================================
# Helper Function
# =========================================================

def run_scenario(name, ml_prediction, ml_confidence, static_data):

    print("\n" + "=" * 70)
    print(f"SCENARIO: {name}")
    print("=" * 70)

    # -----------------------------------------------------
    # Step 1: Behavioral Analysis
    # -----------------------------------------------------

    behavioral_result = analyze_behavior(
        suspicious_apis=static_data.get("suspicious_apis", []),
        extracted_strings=static_data.get("extracted_strings", []),
        network_indicators=static_data.get("network_indicators", {}),
        pe_headers=static_data.get("pe_headers", {}),
        yara_results=static_data.get("yara_results", [])
    )

    print("\n[Behavioral Analysis]")
    print("Behavior Count :", behavioral_result["behavior_count"])
    print("Behavior Score :", behavioral_result["behavior_score"])
    print(
        "Threat Category:",
        behavioral_result["threat_category"]
    )

    if behavioral_result["behaviors"]:
        print("\nDetected Behaviors:")

        for behavior in behavioral_result["behaviors"]:
            print(
                f"- {behavior['behavior']} | "
                f"Severity: {behavior['severity']} | "
                f"Confidence: {behavior['confidence']}"
            )
    else:
        print("\nDetected Behaviors: None")

    # -----------------------------------------------------
    # Step 2: Threat Prediction
    # -----------------------------------------------------

    prediction = predict_threat(
        ml_prediction=ml_prediction,
        ml_confidence=ml_confidence,
        behavioral_result=behavioral_result
    )

    print("\n[Threat Prediction]")
    print("ML Prediction   :", prediction["ml_prediction"])
    print("ML Confidence   :", prediction["ml_confidence"])
    print("Behavior Score  :", prediction["behavior_score"])
    print("Final Score     :", prediction["final_threat_score"])
    print("Threat Level    :", prediction["threat_level"])
    print("Threat Category :", prediction["threat_category"])
    print(
        "Recommended     :",
        prediction["recommended_action"]
    )

    return prediction


# =========================================================
# SCENARIO 1 - BENIGN FILE
# =========================================================

benign_data = {
    "pe_headers": {
        "entry_point": "0x00401000",
        "number_of_sections": 4,
        "sections": [".text", ".rdata", ".data", ".rsrc"]
    },

    "extracted_strings": [
        "Microsoft Corporation",
        "Application started successfully"
    ],

    "suspicious_apis": [],

    "network_indicators": {
        "urls": [],
        "ips": []
    },

    "yara_results": []
}

run_scenario(
    "BENIGN FILE",
    "Benign",
    0.97,
    benign_data
)


# =========================================================
# SCENARIO 2 - SUSPICIOUS POWERSHELL
# =========================================================

powershell_data = {
    "pe_headers": {},

    "extracted_strings": [
        "powershell.exe -ExecutionPolicy Bypass -W Hidden"
    ],

    "suspicious_apis": [],

    "network_indicators": {
        "urls": [],
        "ips": []
    },

    "yara_results": []
}

run_scenario(
    "SUSPICIOUS POWERSHELL ACTIVITY",
    "Benign",
    0.70,
    powershell_data
)


# =========================================================
# SCENARIO 3 - PERSISTENCE
# =========================================================

persistence_data = {
    "pe_headers": {},

    "extracted_strings": [
        "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "schtasks /create /tn UpdateTask"
    ],

    "suspicious_apis": [],

    "network_indicators": {
        "urls": [],
        "ips": []
    },

    "yara_results": []
}

run_scenario(
    "PERSISTENCE ACTIVITY",
    "Malware",
    0.82,
    persistence_data
)


# =========================================================
# SCENARIO 4 - PROCESS INJECTION
# =========================================================

process_injection_data = {
    "pe_headers": {},

    "extracted_strings": [],

    "suspicious_apis": [
        "Kernel32.dll -> VirtualAlloc",
        "Kernel32.dll -> WriteProcessMemory",
        "Kernel32.dll -> CreateRemoteThread"
    ],

    "network_indicators": {
        "urls": [],
        "ips": []
    },

    "yara_results": []
}

run_scenario(
    "PROCESS INJECTION",
    "Malware",
    0.95,
    process_injection_data
)


# =========================================================
# SCENARIO 5 - NETWORK DOWNLOADER
# =========================================================

downloader_data = {
    "pe_headers": {},

    "extracted_strings": [
        "http://malicious-site.com/payload.exe"
    ],

    "suspicious_apis": [
        "Urlmon.dll -> URLDownloadToFileA"
    ],

    "network_indicators": {
        "urls": [
            "http://malicious-site.com/payload.exe"
        ],
        "ips": [
            "185.220.101.5"
        ]
    },

    "yara_results": []
}

run_scenario(
    "NETWORK DOWNLOADER",
    "Malware",
    0.90,
    downloader_data
)


# =========================================================
# SCENARIO 6 - MULTI-STAGE MALWARE
# =========================================================

multi_stage_data = {
    "pe_headers": {
        "entry_point": "0x00401000",
        "number_of_sections": 5,
        "sections": [".text", ".rdata", ".data", ".rsrc"]
    },

    "extracted_strings": [
        "powershell.exe -ExecutionPolicy Bypass",
        "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "http://malicious-site.com/payload.ps1",
        "cmd.exe /c powershell.exe"
    ],

    "suspicious_apis": [
        "Kernel32.dll -> VirtualAlloc",
        "Kernel32.dll -> WriteProcessMemory",
        "Kernel32.dll -> CreateRemoteThread",
        "Urlmon.dll -> URLDownloadToFileA"
    ],

    "network_indicators": {
        "urls": [
            "http://malicious-site.com/payload.ps1"
        ],
        "ips": [
            "185.220.101.5"
        ]
    },

    "yara_results": [
        {
            "rule_name": "Suspicious_PowerShell_Execution",
            "severity": "high"
        }
    ]
}

run_scenario(
    "MULTI-STAGE MALWARE",
    "Malware",
    0.948,
    multi_stage_data
)


# =========================================================
# FINAL MESSAGE
# =========================================================

print("\n" + "=" * 70)
print("ALL THREAT SCENARIOS TESTED")
print("=" * 70)

print("""
Scenario coverage:

1. Benign File              -> Low expected
2. Suspicious PowerShell    -> Suspicious / Medium expected
3. Persistence Activity     -> Suspicious / Medium-High expected
4. Process Injection        -> High/Critical expected
5. Network Downloader       -> Suspicious/High expected
6. Multi-Stage Malware      -> Critical expected
""")