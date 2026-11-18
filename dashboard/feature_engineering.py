"""Feature-engineering dashboard page."""
def render(st, dataframe):
    """Display generated feature columns and their definitions."""
    st.title("Feature Engineering")
    if dataframe is None:
        st.info("Run the pipeline from Upload Dataset first.")
        return
    st.write("Calendar fields, weather categories, station-local changes, and rolling averages are generated from each station's chronological history.")
    st.dataframe(dataframe.head(100), use_container_width=True)
    st.write("Feature columns")
    st.code(", ".join(dataframe.columns))
