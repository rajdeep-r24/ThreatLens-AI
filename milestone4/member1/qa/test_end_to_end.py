import sys
from pathlib import Path

M3_PATH = (
    Path(__file__).resolve().parents[3]
    / "milestone3"
    / "member1"
    / "behavioral_analysis"
)

sys.path.insert(0, str(M3_PATH))

from ml_prediction import MLPredictionEngine
from behavioral_analysis import analyze_behavior
from threat_prediction import predict_threat
from threat_report import generate_threat_report


MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "models"
    / "malware_classifier_pipeline.joblib"
)

DATASET_PATH = Path(
    r"C:\Users\SRUTHI\Downloads\Info Malware dataset\ClaMP_Integrated-5184.csv"
)


def test_end_to_end_pipeline():

    # -----------------------------
    # STEP 1: Load real ML model
    # -----------------------------
    assert MODEL_PATH.exists(), "ML model file not found"
    assert DATASET_PATH.exists(), "Dataset file not found"

    import pandas as pd

    dataset = pd.read_csv(DATASET_PATH)

    # Select a known malware sample
    malware_sample = dataset[dataset["class"] == 1].iloc[0]

    features = malware_sample.drop("class").to_dict()

    ml_engine = MLPredictionEngine(str(MODEL_PATH))
    ml_result = ml_engine.predict(features)

    assert ml_result["ml_prediction"] in ["Malware", "Benign"]
    assert 0 <= ml_result["ml_confidence"] <= 1

    # -----------------------------
    # STEP 2: Behavioral Analysis
    # -----------------------------
    behavioral_result = analyze_behavior(
        suspicious_apis=[
            "VirtualAllocEx",
            "WriteProcessMemory",
            "CreateRemoteThread",
            "CreateProcess"
        ],
        extracted_strings=[
            "powershell.exe",
            "Invoke-Expression",
            r"CurrentVersion\Run",
            "https://malicious.example/payload.exe"
        ],
        network_indicators={
            "urls": ["https://malicious.example/payload.exe"]
        },
        pe_headers={},
        yara_results=[]
    )

    assert isinstance(behavioral_result, dict)
    assert behavioral_result["behavior_count"] > 0
    assert behavioral_result["behavior_score"] > 0

    # -----------------------------
    # STEP 3: Threat Prediction
    # -----------------------------
    threat_result = predict_threat(
    ml_result["ml_prediction"],
    ml_result["ml_confidence"],
    behavioral_result
)
    assert isinstance(threat_result, dict)
    assert 0 <= threat_result["final_threat_score"] <= 100
    assert threat_result["threat_level"] in [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    # -----------------------------
    # STEP 4: Threat Report
    # -----------------------------
    report = generate_threat_report(
        filename="qa_end_to_end_sample.exe",
        sha256_hash="c" * 64,
        threat_prediction=threat_result
    )

    assert isinstance(report, dict)

    # Required report sections
    assert "report_metadata" in report
    assert "file_information" in report
    assert "ml_analysis" in report
    assert "behavioral_analysis" in report
    assert "threat_assessment" in report
    assert "response" in report
    assert "security_summary" in report

    # Verify information flows through the pipeline
    assert (
        report["file_information"]["filename"]
        == "qa_end_to_end_sample.exe"
    )

    assert (
        report["ml_analysis"]["prediction"]
        == ml_result["ml_prediction"]
    )

    assert (
        report["behavioral_analysis"]["behavior_count"]
        == behavioral_result["behavior_count"]
    )

    assert (
        report["threat_assessment"]["final_threat_score"]
        == threat_result["final_threat_score"]
    )

    assert (
        report["threat_assessment"]["threat_level"]
        == threat_result["threat_level"]
    )