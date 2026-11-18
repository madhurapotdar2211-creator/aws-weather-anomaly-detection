"""SQLAlchemy engine, session factory, and schema initialization."""
from urllib.parse import quote_plus
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from config.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

DATABASE_URL = f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600, pool_size=5, max_overflow=10, connect_args={"connect_timeout": 5})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create ORM tables and add columns introduced by newer releases."""
    from config.base import Base
    import models.weather_station  # noqa: F401
    import models.weather_data  # noqa: F401
    Base.metadata.create_all(bind=engine)
    _repair_weather_data_schema()


def _repair_weather_data_schema():
    """Upgrade an existing weather_data table without deleting stored data."""
    required_columns = {
        "is_anomaly": "TINYINT NOT NULL DEFAULT 0",
        "anomaly_prediction": "TINYINT NULL",
        "disaster_risk": "VARCHAR(40) NULL",
    }
    with engine.begin() as connection:
        existing = {column["name"] for column in inspect(connection).get_columns("weather_data")}
        for name, definition in required_columns.items():
            if name not in existing:
                connection.execute(text(f"ALTER TABLE weather_data ADD COLUMN {name} {definition}"))

def database_health() -> tuple[bool, str]:
    """Return a user-friendly connectivity result for the Settings page."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, "Connected"
    except Exception as exc:
        return False, str(exc)
