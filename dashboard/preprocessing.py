def render(st,df):
    """Display cleaned-data quality statistics."""
    st.title("Preprocessing")
    if df is None: st.info("Run the pipeline from Upload Dataset."); return
    st.dataframe(df.head(100),use_container_width=True); st.write(df.describe(include="all").transpose())
