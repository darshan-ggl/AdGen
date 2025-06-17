import yaml
import logging
from pathlib import Path
from typing import Optional, BinaryIO

from google.cloud import storage


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config():
    """
    Loads the configuration from a YAML file located at the project's root.

    Returns:
        dict: The parsed YAML configuration.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        yaml.YAMLError: If there's an error parsing the YAML file.
    """
    config_file = Path(__file__).parent.parent / "config.yaml"
    logger.info(f"Loading config: {config_file}")

    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing config file: {e}")


def upload_file_to_gcs(file_object: BinaryIO, gcs_destination_path: str) -> Optional[str]:
    """
    Uploads a file-like object to GCS.

    Args:
        file_object: The file-like object from st.file_uploader.
        gcs_destination_path (str): The full path including bucket name (e.g., 'your-bucket/your-folder/your-file.png').

    Returns:
        Optional[str]: The GCS URI (gs://...) of the uploaded file if successful, None otherwise.
    """
    if file_object is None:
        logger.info("No file provided for GCS upload.")
        return None

    storage_client_instance = storage.Client()

    try:
        # Split the destination blob name into bucket and blob path
        if gcs_destination_path.startswith("gs://"):
            gcs_destination_path = gcs_destination_path.replace("gs://", "")

        bucket_name, blob_name = gcs_destination_path.split('/', 1)
        bucket = storage_client_instance.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Upload the file object directly
        blob.upload_from_file(file_object)

        gcs_uri = f"gs://{bucket_name}/{blob_name}"
        logger.info(f"Successfully uploaded file to GCS: {gcs_uri}")
        return gcs_uri

    except Exception as e:
        logger.error(f"Error uploading file to GCS: {gcs_destination_path}: {e}")
        return None


def generate_signed_url(gcs_file_path: str):
    if gcs_file_path.startswith("gs://"):
        gcs_file_path = gcs_file_path.replace("gs://", "")
    bucket_name, blob_name = gcs_file_path.split('/', 1)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(version="v4", expiration=3600)
    return url
