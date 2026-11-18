def render(st,df,session):
    """Train and display anomaly detector comparison metrics."""
    from services.anomaly_services import AnomalyService
    st.title("Anomaly Detection")
    if df is None: st.info("Run the pipeline from Upload Dataset."); return
    if st.button("Train anomaly models"):
        try:
            session["anomaly_result"] = AnomalyService().run(df)
            from dashboard.common import persist_predictions
            try:
                persist_predictions(session["anomaly_result"]["predictions"])
                st.success("Anomaly predictions trained and stored in MySQL.")
            except Exception as database_error:
                st.warning(f"Anomaly model trained; MySQL persistence skipped: {database_error}")
            st.success(f"Best model: {session['anomaly_result']['best_model']}")
        except Exception as exc: st.error(str(exc))
    result=session.get("anomaly_result")
    if result: st.dataframe(result["metrics"],use_container_width=True); st.dataframe(result["predictions"].query("anomaly_prediction == 1").head(100),use_container_width=True)
