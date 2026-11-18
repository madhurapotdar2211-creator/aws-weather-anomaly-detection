"""Safe upload handling and database persistence."""
from pathlib import Path
import pandas as pd
from config.config import RAW_DATA_PATH
from utils.validator import DatasetValidator

class UploadService:
    """Validate and persist an uploaded Excel workbook."""
    def load_dataset(self,file_path):
        """Read a validated Excel file."""
        path=Path(file_path)
        if not path.exists(): raise FileNotFoundError(f"{path} not found.")
        DatasetValidator.validate_file(path)
        return pd.read_excel(path,engine="openpyxl")
    def save_upload(self,uploaded_file):
        """Save a Streamlit UploadedFile with a safe filename."""
        name=Path(uploaded_file.name).name
        if not name.lower().endswith(".xlsx"): raise ValueError("Only .xlsx files are accepted.")
        target=RAW_DATA_PATH/name; target.write_bytes(uploaded_file.getvalue()); return target
