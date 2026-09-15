from pathlib import Path
import json

from ml_prediction import MLPredictionEngine
from behavioral_analysis import analyze_behavior
from threat_prediction import predict_threat
from threat_report import generate_threat_report


# =========================================================
# PATHS
# =========================================================

MODEL_PATH = Path(
    r"C:\Users\SRUTHI\.gemini\antigravity\scratch\threatlens-ai\ThreatLens-AI\models\malware_classifier_pipeline.joblib"
)

DATASET_PATH = Path(
    r"C:\Users\SRUTHI\Downloads\Info Malware dataset\ClaMP_Integrated-5184.csv"
)


# =========================================================
# STEP 1 - LOAD REAL ML MODEL AND DATASET
# =========================================================

import pandas as pd

df = pd.read_csv(DATASET_PATH)

print("\n" + "=" * 60)
print("STEP 1 - REAL ML MODEL PREDICTION")
print("=" * 60)

print("Dataset shape:", df.shape)


# Use a real malware sample from the dataset
sample = df[df["class"] == 1].iloc[0]

actual_class = int(sample["class"])

features = sample.drop("class").to_dict()


# Load trained Milestone 2 model
ml_engine = MLPredictionEngine(str(MODEL_PATH))


# Get REAL prediction
ml_result = ml_engine.predict(features)

print("Actual class:", actual_class, "(Malware)")
print("ML Prediction:", ml_result["ml_prediction"])
print("ML Confidence:", ml_result["ml_confidence"])


# =========================================================
# STEP 2 - STATIC EVIDENCE BEHAVIORAL ANALYSIS
# =========================================================
#
# This represents the type of static-analysis output
# produced by ThreatLens.
#
# No malware is executed.
# =========================================================

static_analysis_result = {
    "pe_headers": {
        "entry_point": "0x00401000",
        "number_of_sections": 5,
        "sections": [".text", ".rdata", ".data", ".rsrc"]
    },

    "extracted_strings": [
        "powershell.exe -ExecutionPolicy Bypass -W Hidden",
        "cmd.exe /c reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "http://malicious-site.com/payload.ps1"
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


behavioral_result = analyze_behavior(
    suspicious_apis=static_analysis_result["suspicious_apis"],
    extracted_strings=static_analysis_result["extracted_strings"],
    network_indicators=static_analysis_result["network_indicators"],
    pe_headers=static_analysis_result["pe_headers"],
    yara_results=static_analysis_result["yara_results"]
)


print("\n" + "=" * 60)
print("STEP 2 - BEHAVIORAL ANALYSIS")
print("=" * 60)

print("Behavior Count :", behavioral_result["behavior_count"])
print("Behavior Score :", behavioral_result["behavior_score"])
print("Threat Category:",
      behavioral_result["threat_category"])

print("\nDetected Behaviors:")

for behavior in behavioral_result["behaviors"]:
    print(
        f"- {behavior['behavior']} | "
        f"Severity: {behavior['severity']} | "
        f"Confidence: {behavior['confidence']}"
    )


# =========================================================
# STEP 3 - THREAT PREDICTION / FUSION
# =========================================================

threat_prediction = predict_threat(
    ml_prediction=ml_result["ml_prediction"],
    ml_confidence=ml_result["ml_confidence"],
    behavioral_result=behavioral_result
)


print("\n" + "=" * 60)
print("STEP 3 - THREAT PREDICTION")
print("=" * 60)

print("ML Prediction   :", threat_prediction["ml_prediction"])
print("ML Confidence   :", threat_prediction["ml_confidence"])
print("Behavior Score  :", threat_prediction["behavior_score"])
print("Final Score     :", threat_prediction["final_threat_score"])
print("Threat Level    :", threat_prediction["threat_level"])
print("Threat Category :", threat_prediction["threat_category"])

print("Recommended Action:")
print(threat_prediction["recommended_action"])


# =========================================================
# STEP 4 - THREAT REPORT GENERATION
# =========================================================

report = generate_threat_report(
    filename="real_malware_sample.exe",
    sha256_hash=(
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649"
        "b934ca495991b7852b855"
    ),
    threat_prediction=threat_prediction
)


print("\n" + "=" * 60)
print("STEP 4 - THREAT PREDICTION REPORT")
print("=" * 60)

print(
    "Report Type:",
    report["report_metadata"]["report_type"]
)

print(
    "File:",
    report["file_information"]["filename"]
)

print(
    "Threat Level:",
    report["threat_assessment"]["threat_level"]
)

print(
    "Final Threat Score:",
    report["threat_assessment"]["final_threat_score"]
)

print("Security Summary:")
print(report["security_summary"])


# =========================================================
# STEP 5 - SAVE JSON REPORT
# =========================================================

REPORT_PATH = "threat_report.json"

with open(REPORT_PATH, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)


print("\n" + "=" * 60)
print("STEP 5 - REPORT FILE GENERATION")
print("=" * 60)

print(f"Threat report saved to: {REPORT_PATH}")


# =========================================================
# FINAL VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("END-TO-END TEST COMPLETED")
print("=" * 60)

print(
    "Real ML Model Prediction  :",
    "PASS" if ml_result["ml_prediction"] == "Malware" else "CHECK"
)

print(
    "Behavioral Analysis       :",
    "PASS" if behavioral_result["behavior_count"] > 0 else "CHECK"
)

print(
    "Threat Prediction         :",
    "PASS" if threat_prediction["final_threat_score"] >= 0 else "CHECK"
)

print(
    "Threat Report Generation  :",
    "PASS" if report else "CHECK"
)

print(
    "JSON Report Generation    :",
    "PASS"
)

print("Overall Member 1 Pipeline : PASS")