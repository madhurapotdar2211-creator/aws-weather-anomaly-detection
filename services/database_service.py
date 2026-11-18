"""Database persistence service using repository abstractions."""
import pandas as pd
from models.weather_data import WeatherData
from repository.weather_data_repository import WeatherDataRepository
from repository.weather_repository import WeatherRepository

class DatabaseService:
    """Persist station metadata and observation/prediction history."""
    def save_dataframe(self, db, dataframe):
        """Insert all rows atomically, including optional model predictions."""
        records = []
        try:
            for row in dataframe.itertuples(index=False):
                station_id = int(row.station_id)
                WeatherRepository.get_or_create_station(db, station_id)
                records.append(WeatherData(station_id=station_id, timestamp=pd.Timestamp(row.timestamp).to_pydatetime(), temperature=float(row.temperature), humidity=float(row.humidity), pressure=float(row.pressure), wind_speed=float(row.wind_speed), wind_direction=float(row.wind_direction), rainfall=float(row.rainfall), solar_radiation=float(row.solar_radiation), is_anomaly=int(getattr(row, "is_anomaly", 0)), anomaly_prediction=int(getattr(row, "anomaly_prediction")) if hasattr(row, "anomaly_prediction") and pd.notna(getattr(row, "anomaly_prediction")) else None, disaster_risk=str(getattr(row, "disaster_risk")) if hasattr(row, "disaster_risk") and pd.notna(getattr(row, "disaster_risk")) else None))
            return WeatherDataRepository.bulk_insert(db, records)
        except Exception:
            db.rollback()
            raise
