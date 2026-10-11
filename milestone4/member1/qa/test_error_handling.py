import sys
from pathlib import Path

import pytest

M3_PATH = (
    Path(__file__).resolve().parents[3]
    / "milestone3"
    / "member1"
    / "behavioral_analysis"
)

sys.path.insert(0, str(M3_PATH))

from ml_prediction import MLPredictionEngine
from threat_report import generate_threat_report


def test_missing_model_file():

    with pytest.raises(FileNotFoundError):
        MLPredictionEngine(
            r"C:\invalid\path\missing_model.joblib"
        )


def test_invalid_report_threat_prediction():

    with pytest.raises(AttributeError):
        generate_threat_report(
            filename="invalid.exe",
            sha256_hash="d" * 64,
            threat_prediction=None
        )


def test_invalid_ml_prediction_input():

    model_path = (
        Path(__file__).resolve().parents[3]
        / "models"
        / "malware_classifier_pipeline.joblib"
    )

    engine = MLPredictionEngine(str(model_path))

    with pytest.raises((ValueError, TypeError, KeyError)):
        engine.predict(None)