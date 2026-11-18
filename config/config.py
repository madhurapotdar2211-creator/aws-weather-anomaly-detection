"""Central, environment-driven configuration for the application."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "weather_monitoring")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
RANDOM_STATE = int(os.getenv("RANDOM_STATE", "42"))
ANOMALY_MODEL_FILENAME = "best_anomaly_model.joblib"
DISASTER_MODEL_FILENAME = "best_disaster_model.joblib"
RAW_DATA_PATH = BASE_DIR / "data" / "raw"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed"
MODEL_PATH = BASE_DIR / "models"
SAVED_MODELS_PATH = MODEL_PATH / "saved_models"
LOG_PATH = BASE_DIR / "logs"
REPORT_PATH = BASE_DIR / "generated_reports"
CHARTS_PATH = REPORT_PATH / "charts"
REQUIRED_COLUMNS = ["station_id", "timestamp", "temperature", "humidity", "pressure", "wind_speed", "wind_direction", "rainfall", "solar_radiation", "is_anomaly"]
NUMERIC_COLUMNS = [column for column in REQUIRED_COLUMNS if column != "timestamp"]
for path in (RAW_DATA_PATH, PROCESSED_DATA_PATH, SAVED_MODELS_PATH, LOG_PATH, REPORT_PATH, CHARTS_PATH):
    path.mkdir(parents=True, exist_ok=True)
