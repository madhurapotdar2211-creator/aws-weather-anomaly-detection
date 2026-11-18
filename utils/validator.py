"""Input validation for uploaded weather workbooks."""
from pathlib import Path
import pandas as pd
from config.config import REQUIRED_COLUMNS

class DatasetValidator:
    """Validate workbook type and the required AWS weather schema."""
    REQUIRED_COLUMNS = REQUIRED_COLUMNS

    @classmethod
    def normalize_columns(cls, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Return a copy with predictable snake-case column names."""
        frame = dataframe.copy()
        frame.columns = [str(c).strip().lower().replace(" ", "_") for c in frame.columns]
        return frame

    @classmethod
    def validate_columns(cls, dataframe: pd.DataFrame) -> list[str]:
        """Return required columns missing from a DataFrame."""
        return [column for column in cls.REQUIRED_COLUMNS if column not in dataframe.columns]

    @classmethod
    def validate_file(cls, file_path) -> pd.DataFrame:
        """Read and validate an .xlsx workbook, raising actionable errors."""
        path = Path(file_path)
        if path.suffix.lower() != ".xlsx":
            raise ValueError("Only .xlsx files are supported.")
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")
        frame = cls.normalize_columns(pd.read_excel(path, engine="openpyxl"))
        missing = cls.validate_columns(frame)
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        return frame
