def render(st,df):
    """Display station-level health indicators."""
    st.title("Sensor Health")
    if df is None: st.info("No processed data available."); return
    grouped=df.groupby("station_id").agg(readings=("station_id","size"),anomalies=("is_anomaly","sum"),temperature_range=("temperature",lambda s:round(s.max()-s.min(),2)),missing_values=("station_id",lambda s:0)).reset_index()
    grouped["health_score"]=(100*(1-grouped.anomalies/grouped.readings)).round(2); st.dataframe(grouped,use_container_width=True)
