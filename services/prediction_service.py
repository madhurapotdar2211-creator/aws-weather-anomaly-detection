"""Application service for disaster risk prediction."""
from ml.disaster_prediction.predictor import DisasterRiskPredictor

class PredictionService:
    """Train and expose disaster risk classifiers."""
    def run(self, dataframe):
        """Compare risk models and return the selected model result."""
        return DisasterRiskPredictor().train_compare(dataframe)
