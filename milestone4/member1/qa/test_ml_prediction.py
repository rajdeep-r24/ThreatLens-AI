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


MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "models"
    / "malware_classifier_pipeline.joblib"
)

DATASET_PATH = Path(r"C:\Users\SRUTHI\Downloads\Info Malware dataset\ClaMP_Integrated-5184.csv")


def test_model_file_exists():
    assert MODEL_PATH.exists(), f"Model not found: {MODEL_PATH}"


def test_dataset_exists():
    assert DATASET_PATH.exists(), f"Dataset not found: {DATASET_PATH}"


def test_benign_sample_prediction():
    import pandas as pd

    df = pd.read_csv(DATASET_PATH)

    benign_sample = df[df["class"] == 0].iloc[0].drop("class").to_dict()

    engine = MLPredictionEngine(str(MODEL_PATH))
    result = engine.predict(benign_sample)

    assert result["ml_prediction"] == "Benign"
    assert 0.0 <= result["ml_confidence"] <= 1.0


def test_malware_sample_prediction():
    import pandas as pd

    df = pd.read_csv(DATASET_PATH)

    malware_sample = df[df["class"] == 1].iloc[0].drop("class").to_dict()

    engine = MLPredictionEngine(str(MODEL_PATH))
    result = engine.predict(malware_sample)

    assert result["ml_prediction"] == "Malware"
    assert 0.0 <= result["ml_confidence"] <= 1.0