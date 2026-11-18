"""Streamlit entry point for the AWS weather intelligence system."""
import streamlit as st
from dashboard import analysis, anomaly_detection, feature_engineering, home, predictions, preprocessing, report_page, sensor_health, settings, upload
from dashboard.common import current_dataframe

st.set_page_config(page_title="AWS Weather Intelligence", page_icon="🌦️", layout="wide")
st.sidebar.title("Weather Intelligence")
page = st.sidebar.radio("Navigation", ["Home", "Upload Dataset", "Preprocessing", "Feature Engineering", "Analysis", "Anomaly Detection", "Disaster Prediction", "Sensor Health", "Reports", "Settings"])
if "df" not in st.session_state:
    st.session_state["df"] = current_dataframe()
df = st.session_state.get("df")
if page == "Home": home.render(st, df)
elif page == "Upload Dataset": upload.render(st, st.session_state)
elif page == "Preprocessing": preprocessing.render(st, df)
elif page == "Feature Engineering": feature_engineering.render(st, df)
elif page == "Analysis": analysis.render(st, df)
elif page == "Anomaly Detection": anomaly_detection.render(st, df, st.session_state)
elif page == "Disaster Prediction": predictions.render(st, df, st.session_state)
elif page == "Sensor Health": sensor_health.render(st, df)
elif page == "Reports": report_page.render(st, df, st.session_state)
else: settings.render(st)
