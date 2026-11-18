def render(st,df,session):
    """Generate and offer the PDF report for download."""
    from services.report_service import ReportService
    st.title("Reports")
    if df is None: st.info("Run the pipeline from Upload Dataset."); return
    if st.button("Generate PDF report"):
        try: session["report_path"]=ReportService().generate(df,session.get("anomaly_result"),session.get("risk_result")); st.success("Report generated.")
        except Exception as exc: st.error(str(exc))
    path=session.get("report_path")
    if path and path.exists(): st.download_button("Download Report",path.read_bytes(),file_name=path.name,mime="application/pdf")
