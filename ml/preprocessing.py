"""Excel ingestion, schema validation, cleaning, and persistence."""
from pathlib import Path
import pandas as pd
from config.config import NUMERIC_COLUMNS, PROCESSED_DATA_PATH, REQUIRED_COLUMNS
from utils.validator import DatasetValidator

class DataPreprocessor:
    """Validate and clean an AWS observation dataset."""
    numeric_columns = NUMERIC_COLUMNS

    def __init__(self, input_file=None, output_file=None):
        self.input_file = Path(input_file) if input_file else None
        self.output_file = Path(output_file or PROCESSED_DATA_PATH / "clean_weather_data.xlsx")
        self.df, self.stats = None, {}

    def load_dataset(self, source=None) -> pd.DataFrame:
        """Read an Excel path or uploaded file-like object and validate its schema."""
        source = source if source is not None else self.input_file
        if source is None:
            raise ValueError("An Excel input file is required.")
        self.df = DatasetValidator.normalize_columns(pd.read_excel(source, engine="openpyxl"))
        missing = [c for c in REQUIRED_COLUMNS if c not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        return self.df

    def clean(self) -> pd.DataFrame:
        """Convert types, impute missing values, remove duplicates and invalid readings."""
        if self.df is None:
            self.load_dataset()
        before = len(self.df)
        frame = self.df.copy()
        for column in self.numeric_columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
        frame = frame.drop_duplicates().dropna(subset=["station_id", "timestamp"])
        for column in self.numeric_columns:
            median = frame[column].median()
            frame[column] = frame[column].fillna(0 if pd.isna(median) else median)
        frame["station_id"] = frame["station_id"].round().astype(int)
        frame["is_anomaly"] = frame["is_anomaly"].clip(0, 1).round().astype(int)
        valid = (frame.temperature.between(-50, 60) & frame.humidity.between(0, 100) & frame.pressure.between(850, 1100) & frame.wind_speed.ge(0) & frame.wind_direction.between(0, 360) & frame.rainfall.ge(0) & frame.solar_radiation.ge(0) & frame.station_id.ge(0))
        self.df = frame.loc[valid].sort_values(["station_id", "timestamp"]).reset_index(drop=True)
        self.stats = {"input_rows": before, "output_rows": len(self.df), "removed_rows": before - len(self.df), "missing_values_after": int(self.df.isna().sum().sum())}
        return self.df

    def save(self):
        """Persist cleaned observations to the configured workbook path."""
        if self.df is None:
            raise RuntimeError("Clean the dataset before saving it.")
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_excel(self.output_file, index=False, engine="openpyxl")
        return self.output_file

    def preprocess(self, source=None) -> pd.DataFrame:
        """Run validation, cleaning, and workbook persistence."""
        self.load_dataset(source)
        self.clean()
        self.save()
        return self.df
