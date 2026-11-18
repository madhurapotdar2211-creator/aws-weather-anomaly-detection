# AWS Weather Anomaly Detection and Disaster Risk Prediction System

Production-style Python/Streamlit application for cleaning Automatic Weather Station Excel data, engineering temporal features, detecting sensor anomalies, and estimating weather disaster risk.

## Run

1. Create a Python 3.10+ environment and install dependencies: `pip install -r requirements.txt`.
2. Create the MySQL database and tables with `database/schema.sql`.
3. Set `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` in `.env`.
4. Start the dashboard with `streamlit run app.py`.

The upload workflow writes `data/processed/clean_weather_data.xlsx` and `data/processed/final_ml_dataset.xlsx`, chart PNGs to `generated_reports/charts`, and trained models to `models/saved_models`. The application includes a SQLAlchemy persistence layer for station, observation, anomaly, and risk history.

## Expected workbook columns

`station_id`, `timestamp`, `temperature`, `humidity`, `pressure`, `wind_speed`, `wind_direction`, `rainfall`, `solar_radiation`, and `is_anomaly`.

When no disaster label is present, risk labels are derived from documented weather thresholds so the supervised comparison is runnable on the specified input format.
