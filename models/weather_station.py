from sqlalchemy import Column, Integer, String, Date, Float, Enum
from config.base import Base


class WeatherStation(Base):
    __tablename__ = "weather_station"

    station_id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String(100), nullable=False)
    location = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    installation_date = Column(Date)
    status = Column(
        Enum("Active", "Inactive"),
        default="Active"
    )
