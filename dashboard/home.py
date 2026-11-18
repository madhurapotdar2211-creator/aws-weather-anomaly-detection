def render(st, df=None):
    """Render the overview page."""
    st.title("AWS Weather Anomaly Detection"); st.caption("AI-assisted sensor quality monitoring and disaster risk prediction")
    if df is None: st.info("Upload an Excel dataset to begin the pipeline."); return
    a,b,c,d=st.columns(4); a.metric("Observations",f"{len(df):,}"); b.metric("Stations",f"{df.station_id.nunique():,}"); c.metric("Anomaly %",f"{df.is_anomaly.mean()*100:.2f}%"); d.metric("Date range",f"{df.timestamp.min():%Y-%m-%d} → {df.timestamp.max():%Y-%m-%d}")
    from dashboard.common import render_charts; render_charts(st,4)
