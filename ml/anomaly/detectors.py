"""Unsupervised Isolation Forest, LOF, and One-Class SVM comparison."""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.neighbors import LocalOutlierFactor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from config.config import ANOMALY_MODEL_FILENAME, RANDOM_STATE, SAVED_MODELS_PATH

class AnomalyDetector:
    """Train anomaly detectors and select the best labelled agreement."""
    features = ["temperature", "humidity", "pressure", "wind_speed", "wind_direction", "rainfall", "solar_radiation"]
    def __init__(self, model_dir=None):
        self.model_dir = Path(model_dir or SAVED_MODELS_PATH)
        self.model_dir.mkdir(parents=True, exist_ok=True)

    def train_compare(self, dataframe):
        """Fit all candidates, calculate metrics, save the best bundle, and return predictions."""
        frame = dataframe.dropna(subset=self.features).copy()
        if len(frame) < 3:
            raise ValueError("At least three valid weather rows are required for anomaly detection.")
        X = frame[self.features]
        y = frame["is_anomaly"].astype(int) if "is_anomaly" in frame else None
        contamination = float(np.clip(y.mean() if y is not None and y.mean() > 0 else 0.05, 0.001, 0.49))
        neighbors = max(2, min(20, len(X) - 1))
        models = {
            "Isolation Forest": IsolationForest(n_estimators=200, contamination=contamination, random_state=RANDOM_STATE, n_jobs=-1),
            "Local Outlier Factor": LocalOutlierFactor(n_neighbors=neighbors, contamination=contamination, novelty=True),
            "One-Class SVM": Pipeline([("scale", StandardScaler()), ("svm", OneClassSVM(nu=contamination, kernel="rbf"))]),
        }
        results, predictions, curves = [], {}, {}
        for name, model in models.items():
            fit_input = X.to_numpy() if name == "Local Outlier Factor" else X
            model.fit(fit_input)
            prediction_input = X.to_numpy() if name == "Local Outlier Factor" else X
            predicted = (model.predict(prediction_input) == -1).astype(int)
            predictions[name] = predicted
            row = {"model": name, "accuracy": None, "precision": None, "recall": None, "f1": None, "roc_auc": None, "confusion_matrix": None}
            if y is not None:
                row.update(accuracy=accuracy_score(y, predicted), precision=precision_score(y, predicted, zero_division=0), recall=recall_score(y, predicted, zero_division=0), f1=f1_score(y, predicted, zero_division=0), confusion_matrix=confusion_matrix(y, predicted).tolist())
                if y.nunique() > 1:
                    row["roc_auc"] = roc_auc_score(y, predicted)
                    fpr, tpr, _ = roc_curve(y, predicted)
                    curves[name] = {"fpr": fpr.tolist(), "tpr": tpr.tolist()}
            results.append(row)
        scores = [row["f1"] if row["f1"] is not None else 0 for row in results]
        best = results[int(np.argmax(scores))]["model"]
        joblib.dump({"model": models[best], "features": self.features}, self.model_dir / ANOMALY_MODEL_FILENAME)
        output = frame.copy()
        output["anomaly_prediction"] = predictions[best]
        return {"best_model": best, "metrics": pd.DataFrame(results), "predictions": output, "models": models, "roc_curves": curves}

    def predict(self, dataframe):
        """Load the selected persisted detector and classify new rows."""
        bundle = joblib.load(self.model_dir / ANOMALY_MODEL_FILENAME)
        return (bundle["model"].predict(dataframe[bundle["features"]]) == -1).astype(int)
