from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    String,
)

from sqlalchemy.orm import relationship

from config.base import Base


class WeatherData(Base):

    __tablename__ = "weather_data"

    data_id = Column(Integer, primary_key=True, index=True)

    station_id = Column(
        Integer,
        ForeignKey("weather_station.station_id")
    )

    timestamp = Column(DateTime)

    temperature = Column(Float)

    humidity = Column(Float)

    pressure = Column(Float)

    wind_speed = Column(Float)

    wind_direction = Column(Float)

    rainfall = Column(Float)

    solar_radiation = Column(Float)
    is_anomaly = Column(Integer, default=0)
    anomaly_prediction = Column(Integer)
    disaster_risk = Column(String(40))

    station = relationship("WeatherStation")
