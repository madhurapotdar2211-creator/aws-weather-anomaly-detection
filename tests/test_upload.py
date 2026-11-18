from services.upload_services import UploadService
from utils.validator import DatasetValidator

service = UploadService()

df = service.load_dataset("data/raw/aws.xlsx")

print(df.head())

missing = DatasetValidator.validate_columns(df)

if missing:
    print("Missing Columns:", missing)
else:
    print("Dataset Valid")
