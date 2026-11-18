def render(st,df,session):
    """Train and display disaster risk model comparison."""
    from services.prediction_service import PredictionService
    st.title("Disaster Prediction")
    if df is None: st.info("Run the pipeline from Upload Dataset."); return
    if st.button("Train disaster risk models"):
        try:
            session["risk_result"] = PredictionService().run(df)
            from dashboard.common import persist_predictions
            try:
                persist_predictions(session["risk_result"]["predictions"])
                st.success("Disaster predictions trained and stored in MySQL.")
            except Exception as database_error:
                st.warning(f"Risk model trained; MySQL persistence skipped: {database_error}")
            st.success(f"Best model: {session['risk_result']['best_model']}")
        except Exception as exc: st.error(str(exc))
    result=session.get("risk_result")
    if result: st.dataframe(result["metrics"],use_container_width=True); st.dataframe(result["predictions"].tail(100),use_container_width=True)
