from sqlalchemy.orm import Session
from models.weather_data import WeatherData

class AnomalyRepository:
    """Persistence operations for prediction history stored with weather rows."""
    @staticmethod
    def anomaly_rows(db: Session):
        return db.query(WeatherData).filter(WeatherData.anomaly_prediction == 1).all()

    @staticmethod
    def risk_rows(db: Session):
        return db.query(WeatherData).filter(WeatherData.disaster_risk.isnot(None)).all()
