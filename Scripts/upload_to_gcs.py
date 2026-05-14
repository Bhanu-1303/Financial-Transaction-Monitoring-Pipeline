from google.cloud import storage
from pathlib import Path

# Change this to your actual GCS bucket name
BUCKET_NAME = "financial-tranctions-data"

# Local CSV file path
SOURCE_FILE_PATH = Path("data/mock_credit_card_transactions.csv")

# Destination path inside GCS bucket
DESTINATION_BLOB_NAME = "raw/mock_credit_card_transactions.csv"


def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """
    Note: Uploads a local file to Google Cloud Storage.
    """

    if not source_file_path.exists():
        raise FileNotFoundError(f"File not found: {source_file_path}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(str(source_file_path))

    print("File uploaded successfully!")
    print(f"Local file: {source_file_path}")
    print(f"GCS path: gs://{bucket_name}/{destination_blob_name}")


if __name__ == "__main__":
    upload_to_gcs(
        BUCKET_NAME,
        SOURCE_FILE_PATH,
        DESTINATION_BLOB_NAME
    )
