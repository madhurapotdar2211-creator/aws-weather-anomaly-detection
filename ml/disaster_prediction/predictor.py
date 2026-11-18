"""Random Forest, XGBoost, and Logistic Regression risk comparison."""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from config.config import DISASTER_MODEL_FILENAME, RANDOM_STATE, SAVED_MODELS_PATH

class DisasterRiskPredictor:
    """Create domain-informed risk labels and compare supervised classifiers."""
    features = ["temperature", "humidity", "pressure", "wind_speed", "rainfall", "solar_radiation"]
    def __init__(self, model_dir=None):
        self.model_dir = Path(model_dir or SAVED_MODELS_PATH)
        self.model_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def build_target(frame):
        """Derive Normal, Heavy Rain, Storm Risk, and Flood Risk classes."""
        return np.select([(frame.rainfall >= 50) & (frame.humidity >= 75), (frame.wind_speed >= 35) | (frame.pressure < 970), (frame.rainfall >= 25) & (frame.pressure < 990)], ["Flood Risk", "Storm Risk", "Heavy Rain"], default="Normal")

    def train_compare(self, dataframe):
        """Train candidates, evaluate them, save the best model bundle, and predict all rows."""
        frame = dataframe.dropna(subset=self.features).copy()
        if len(frame) < 4:
            raise ValueError("At least four valid weather rows are required for risk prediction.")
        labels = pd.Series(self.build_target(frame), index=frame.index, name="disaster_risk")
        encoder = LabelEncoder().fit(labels)
        y = encoder.transform(labels)
        X = frame[self.features]
        stratify = y if len(np.unique(y)) > 1 and pd.Series(y).value_counts().min() >= 2 else None
        if len(frame) >= 12:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=RANDOM_STATE, stratify=stratify)
        else:
            X_train = X_test = X
            y_train = y_test = y
        try:
            from xgboost import XGBClassifier
            xgb = XGBClassifier(n_estimators=150, max_depth=4, learning_rate=.08, subsample=.9, colsample_bytree=.9, eval_metric="mlogloss", random_state=RANDOM_STATE, verbosity=0)
        except ImportError:
            xgb = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
        models = {"Random Forest": RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=RANDOM_STATE), "XGBoost": xgb, "Logistic Regression": Pipeline([("scale", StandardScaler()), ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))])}
        fitted, rows = {}, []
        for name, model in models.items():
            try:
                model.fit(X_train, y_train)
            except ValueError:
                model = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
            predicted = model.predict(X_test)
            fitted[name] = model
            rows.append({"model": name, "accuracy": accuracy_score(y_test, predicted), "precision": precision_score(y_test, predicted, average="weighted", zero_division=0), "recall": recall_score(y_test, predicted, average="weighted", zero_division=0), "f1": f1_score(y_test, predicted, average="weighted", zero_division=0)})
        metrics = pd.DataFrame(rows)
        best = metrics.sort_values("f1", ascending=False).iloc[0]["model"]
        bundle = {"model": fitted[best], "encoder": encoder, "features": self.features}
        joblib.dump(bundle, self.model_dir / DISASTER_MODEL_FILENAME)
        output = frame.copy()
        output["disaster_risk"] = encoder.inverse_transform(fitted[best].predict(X))
        return {"best_model": best, "metrics": metrics, "predictions": output, "models": fitted}

    def predict(self, dataframe):
        """Load the saved risk model bundle and return string class labels."""
        bundle = joblib.load(self.model_dir / DISASTER_MODEL_FILENAME)
        return bundle["encoder"].inverse_transform(bundle["model"].predict(dataframe[bundle["features"]]))
