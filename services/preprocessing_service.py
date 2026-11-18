"""Application service connecting cleaning and feature engineering."""
from ml.feature_engineering import FeatureEngineer
from ml.preprocessing import DataPreprocessor

class PreprocessingService:
    """Run both preparation phases on the same cleaned DataFrame."""
    def run(self, source):
        """Return dataframes, output paths, and data-quality statistics."""
        preprocessor = DataPreprocessor()
        clean = preprocessor.preprocess(source)
        engineer = FeatureEngineer()
        engineered = engineer.engineer_features(clean)
        return {"clean": clean, "engineered": engineered, "clean_path": preprocessor.output_file, "engineered_path": engineer.output_file, "stats": preprocessor.stats}
