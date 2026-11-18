"""Temporal, categorical, and rolling feature generation."""
from pathlib import Path
import numpy as np
import pandas as pd
from config.config import PROCESSED_DATA_PATH

class FeatureEngineer:
    """Create chronological features without using future observations."""
    def __init__(self, input_file=None, output_file=None):
        self.input_file = Path(input_file or PROCESSED_DATA_PATH / "clean_weather_data.xlsx")
        self.output_file = Path(output_file or PROCESSED_DATA_PATH / "final_ml_dataset.xlsx")
        self.df = None

    def load(self, dataframe=None):
        """Load a supplied cleaned frame or the persisted clean workbook."""
        self.df = dataframe.copy() if dataframe is not None else pd.read_excel(self.input_file, engine="openpyxl")
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
        return self.df

    def transform(self):
        """Add all requested calendar, category, delta, and rolling features."""
        if self.df is None:
            self.load()
        self.df = self.df.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
        timestamp = self.df["timestamp"]
        self.df = self.df.assign(
            hour=timestamp.dt.hour, day=timestamp.dt.day, month=timestamp.dt.month,
            year=timestamp.dt.year, weekday=timestamp.dt.dayofweek,
            season=timestamp.dt.month.map({12:"Winter",1:"Winter",2:"Winter",3:"Summer",4:"Summer",5:"Summer",6:"Monsoon",7:"Monsoon",8:"Monsoon",9:"Monsoon",10:"Post-Monsoon",11:"Post-Monsoon"}),
            is_day=timestamp.dt.hour.between(6, 18).astype(int),
        )
        self.df["temperature_category"] = pd.cut(self.df.temperature, [-np.inf, 15, 30, np.inf], labels=["Cold", "Moderate", "Hot"]).astype(str)
        self.df["humidity_category"] = pd.cut(self.df.humidity, [-np.inf, 30, 70, np.inf], labels=["Low", "Medium", "High"]).astype(str)
        self.df["pressure_category"] = pd.cut(self.df.pressure, [-np.inf, 1000, 1020, np.inf], labels=["Low", "Normal", "High"]).astype(str)
        self.df["rainfall_category"] = pd.cut(self.df.rainfall, [-np.inf, 0, 10, 30, np.inf], labels=["No Rain", "Light Rain", "Moderate Rain", "Heavy Rain"], include_lowest=True).astype(str)
        self.df["wind_category"] = pd.cut(self.df.wind_speed, [-np.inf, 10, 25, np.inf], labels=["Calm", "Moderate", "Strong"]).astype(str)
        grouped = self.df.groupby("station_id", group_keys=False)
        for column in ("temperature", "pressure", "humidity"):
            self.df[f"{column}_change"] = grouped[column].diff().fillna(0)
            self.df[f"rolling_average_{column}"] = grouped[column].transform(lambda series: series.rolling(3, min_periods=1).mean())
        return self.df

    def save(self):
        """Persist the engineered dataset."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_excel(self.output_file, index=False, engine="openpyxl")
        return self.output_file

    def engineer_features(self, dataframe=None):
        """Load, transform, and save a complete feature dataset."""
        self.load(dataframe)
        self.transform()
        self.save()
        return self.df

FeatureEngineering = FeatureEngineer
