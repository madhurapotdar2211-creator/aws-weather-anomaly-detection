def render(st, session):
    """Render upload and pipeline execution controls."""
    from services.upload_services import UploadService
    from services.preprocessing_service import PreprocessingService
    st.title("Upload Dataset"); uploaded=st.file_uploader("AWS weather workbook (.xlsx)",type=["xlsx","xls"])
    if uploaded and st.button("Run complete pipeline",type="primary"):
        try:
            path = UploadService().save_upload(uploaded)
            result = PreprocessingService().run(path)
            session["df"]=result["engineered"]; session["source_name"]=uploaded.name
            from ml.analysis import WeatherAnalysis
            WeatherAnalysis(result["engineered"]).generate_charts()
            try:
                from config.database import SessionLocal, init_db
                from services.database_service import DatabaseService
                init_db(); db=SessionLocal()
                try: DatabaseService().save_dataframe(db, result["clean"])
                finally: db.close()
                st.success("Processed observations were also stored in MySQL.")
            except Exception as database_error:
                st.warning(f"File/ML pipeline completed; MySQL persistence was skipped: {database_error}")
            st.success(f"Pipeline complete: {result['stats']['output_rows']:,} clean rows."); st.dataframe(session["df"].head(25),use_container_width=True)
        except Exception as exc: st.error(str(exc))
