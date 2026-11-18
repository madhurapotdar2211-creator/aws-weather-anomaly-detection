def render(st):
    """Display runtime and model configuration."""
    from config.config import DB_HOST,DB_PORT,DB_NAME,SAVED_MODELS_PATH
    st.title("Settings"); st.write({"database_host":DB_HOST,"database_port":DB_PORT,"database":DB_NAME,"model_directory":str(SAVED_MODELS_PATH)})
