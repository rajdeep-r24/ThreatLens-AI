"""
ThreatLens AI - Milestone 3
Member 1: ML Prediction Adapter

Loads the trained Milestone 2 malware classification pipeline
and generates a malware/benign prediction with confidence.

The trained model is NOT retrained here.
"""

from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd


class MLPredictionEngine:
    """Wrapper around the trained Milestone 2 malware classifier."""

    def __init__(self, model_path: str):
        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"ML model not found: {self.model_path}"
            )

        self.model = joblib.load(self.model_path)

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate malware prediction from one feature record.

        The feature dictionary should contain the original
        ClaMP feature columns expected by the trained pipeline.
        """

        feature_df = pd.DataFrame([features])

        prediction = self.model.predict(feature_df)[0]

        probabilities = self.model.predict_proba(feature_df)[0]

        confidence = float(max(probabilities))

        if prediction == 1:
            label = "Malware"
        else:
            label = "Benign"

        return {
            "ml_prediction": label,
            "ml_confidence": round(confidence, 4),
        }


if __name__ == "__main__":

    print("ML Prediction Adapter")
    print("---------------------")
    print("Module loaded successfully.")
    print()
    print(
        "Provide the path to malware_classifier_pipeline.joblib "
        "and a ClaMP feature record to perform prediction."
    )