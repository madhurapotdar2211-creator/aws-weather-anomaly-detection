"""Shared dashboard rendering helpers."""
from pathlib import Path
import pandas as pd
from config.config import PROCESSED_DATA_PATH, CHARTS_PATH

def current_dataframe():
    """Return the latest engineered dataset if one exists."""
    path=PROCESSED_DATA_PATH/"final_ml_dataset.xlsx"
    return pd.read_excel(path,engine="openpyxl") if path.exists() else None

def render_charts(st, limit=None):
    """Render generated PNG charts in a compact dashboard grid."""
    charts=sorted(CHARTS_PATH.glob("*.png")); charts=charts[:limit] if limit else charts
    for index in range(0,len(charts),2):
        cols=st.columns(2)
        for col,chart in zip(cols,charts[index:index+2]): col.image(str(chart),caption=chart.stem.replace("_"," ").title(),use_container_width=True)

def persist_predictions(dataframe):
    """Persist a prediction-enriched DataFrame when MySQL is available."""
    from config.database import SessionLocal, init_db
    from services.database_service import DatabaseService
    init_db()
    db = SessionLocal()
    try:
        return DatabaseService().save_dataframe(db, dataframe)
    finally:
        db.close()
