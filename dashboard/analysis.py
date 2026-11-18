"""Exploratory analysis dashboard page."""
def render(st, dataframe=None):
    """Display generated charts and allow regeneration from current data."""
    from dashboard.common import render_charts
    from ml.analysis import WeatherAnalysis
    st.title("Analysis")
    if dataframe is not None and st.button("Regenerate charts"):
        WeatherAnalysis(dataframe).generate_charts()
        st.success("Charts regenerated.")
    render_charts(st)
