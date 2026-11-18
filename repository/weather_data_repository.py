from sqlalchemy.orm import Session
from models.weather_data import WeatherData


class WeatherDataRepository:

    @staticmethod
    def insert_weather_data(db: Session, weather):
        db.add(weather)
        db.commit()
        db.refresh(weather)
        return weather

    @staticmethod
    def get_all_weather_data(db: Session):
        return db.query(WeatherData).all() 

    @staticmethod
    def bulk_insert(db: Session, records):
        """Insert weather rows atomically and return the inserted count."""
        db.add_all(records)
        db.commit()
        return len(records)
