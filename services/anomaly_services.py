"""Application service for anomaly detection."""
from ml.anomaly.detectors import AnomalyDetector

class AnomalyService:
    """Train and expose sensor anomaly models."""
    def run(self, dataframe):
        """Compare detectors and return the selected model result."""
        return AnomalyDetector().train_compare(dataframe)
