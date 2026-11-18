from sqlalchemy.orm import Session
from models.weather_station import WeatherStation


class WeatherRepository:

    @staticmethod
    def create_station(db: Session, station: WeatherStation):
        db.add(station)
        db.commit()
        db.refresh(station)
        return station

    @staticmethod
    def get_all_stations(db: Session):
        return db.query(WeatherStation).all()

    @staticmethod
    def get_station_by_id(db: Session, station_id: int):
        return db.query(WeatherStation).filter(
            WeatherStation.station_id == station_id
        ).first()

    @staticmethod
    def get_or_create_station(db: Session, station_id: int):
        """Return a station, creating a safe default metadata row if needed."""
        station = WeatherRepository.get_station_by_id(db, int(station_id))
        if station is None:
            station = WeatherStation(station_id=int(station_id), station_name=f"AWS-{station_id}", status="Active")
            db.add(station)
            db.flush()
        return station
