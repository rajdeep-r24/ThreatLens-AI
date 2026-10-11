from pathlib import Path

import pandas as pd

from ml_prediction import MLPredictionEngine


# =========================================================
# Paths
# =========================================================

MODEL_PATH = Path(
    r"C:\Users\SRUTHI\.gemini\antigravity\scratch\threatlens-ai\ThreatLens-AI\models\malware_classifier_pipeline.joblib"
)

DATASET_PATH = Path(
    r"C:\Users\SRUTHI\Downloads\Info Malware dataset\ClaMP_Integrated-5184.csv"
)


# =========================================================
# Load Dataset
# =========================================================

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)


# =========================================================
# Load ML Model
# =========================================================

engine = MLPredictionEngine(str(MODEL_PATH))


# =========================================================
# Test Benign Sample
# =========================================================

benign_sample = df[df["class"] == 0].iloc[0]

benign_features = benign_sample.drop("class").to_dict()

benign_result = engine.predict(benign_features)

print("\n" + "=" * 60)
print("BENIGN SAMPLE")
print("=" * 60)

print("Actual class: 0 (Benign)")
print("ML Prediction:")
print(benign_result)


# =========================================================
# Test Malware Sample
# =========================================================

malware_sample = df[df["class"] == 1].iloc[0]

malware_features = malware_sample.drop("class").to_dict()

malware_result = engine.predict(malware_features)

print("\n" + "=" * 60)
print("MALWARE SAMPLE")
print("=" * 60)

print("Actual class: 1 (Malware)")
print("ML Prediction:")
print(malware_result)


# =========================================================
# Validation
# =========================================================

print("\n" + "=" * 60)
print("ML ADAPTER VALIDATION")
print("=" * 60)

benign_correct = (
    benign_result["ml_prediction"] == "Benign"
)

malware_correct = (
    malware_result["ml_prediction"] == "Malware"
)

print(
    "Benign sample prediction:",
    "PASS" if benign_correct else "CHECK"
)

print(
    "Malware sample prediction:",
    "PASS" if malware_correct else "CHECK"
)

if benign_correct and malware_correct:
    print("\nOverall ML Adapter Test: PASS")
else:
    print("\nOverall ML Adapter Test: CHECK RESULTS")