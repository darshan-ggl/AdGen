# src/backend/video_ops.py

import os
import logging
import tempfile
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

import ffmpeg
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_streamlit_file_to_gcs(uploaded_file, destination_blob_name: str) -> Optional[str]:
    """
    Uploads a file-like object from Streamlit's file_uploader to GCS.

    Args:
        uploaded_file: The file-like object from st.file_uploader.
        destination_blob_name (str): The full path including bucket name (e.g., 'your-bucket/your-folder/your-file.png').

    Returns:
        Optional[str]: The GCS URI (gs://...) of the uploaded file if successful, None otherwise.
    """
    if uploaded_file is None:
        logger.info("No file provided for GCS upload.")
        return None

    storage_client_instance = storage.Client()

    try:
        # Split the destination blob name into bucket and blob path
        # Assuming destination_blob_name is like 'your-bucket/your-folder/your-file.png'
        bucket_name, blob_name = destination_blob_name.split('/', 1)

        bucket = storage_client_instance.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Upload the file object directly
        blob.upload_from_file(uploaded_file)

        gcs_uri = f"gs://{bucket_name}/{blob_name}"
        logger.info(f"Uploaded Streamlit file to GCS: {gcs_uri}")

        # Note: Implementing deletion on app close is complex in Streamlit's serverless
        # nature. This is a TODO for a production system, likely requiring a separate
        # cleanup mechanism.

        return gcs_uri

    except Exception as e:
        logger.error(f"Error uploading Streamlit file to GCS destination {destination_blob_name}: {e}")
        return None


def generate_video_clip(
        prompt: str,
        output_location: str,
        aspect_ratio: str,
        duration_seconds: str,
        person_generation: str,
        negative_prompt: str = None,
        image_gcs_uri: str = None,
        metadata: dict = None,
):
    # Simulate the time taken by a video generation API call
    import time
    time.sleep(5)

    generated_clips_data = []
    storage_client_instance = storage.Client()

    parsed_url = urlparse(output_location)
    bucket_name = parsed_url.netloc
    prefix = parsed_url.path.lstrip('/')

    try:
        bucket = storage_client_instance.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        for blob in blobs:
            if blob.name == prefix + "/":
                continue

            gs_uri = f"gs://{bucket_name}/{blob.name}"
            http_url = f"https://storage.cloud.google.com/{bucket_name}/{blob.name}"

            generated_clips_data.append({
                'gs_uri': gs_uri,
                'http_url': http_url
            })

    except Exception as e:
        logging.error(f"Error listing blobs or generating signed URLs at {output_location}: {e}")
        return []

    logging.info(f"Simulated generated video data (gs_uri and signed http_url) by listing: {generated_clips_data}")
    return generated_clips_data


def download_from_gcs(gcs_urls, local_dir="temp_videos"):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    storage_client = storage.Client()
    local_paths = []

    for url in gcs_urls:
        if not url.startswith("gs://"):
            logging.error(f"Invalid GCS URL format (expected gs://): {url}")
            continue

        try:
            parts = url[5:].split('/', 1)
            bucket_name = parts[0]
            blob_name = parts[1]

            local_filename = os.path.join(local_dir, os.path.basename(blob_name))
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.download_to_filename(local_filename)
            local_paths.append(local_filename)
            logging.info(f"Downloaded {url} to {local_filename}")
        except Exception as e:
            logging.error(f"Error downloading {url}: {e}")

    return local_paths


def merge_video_clips(gcs_video_urls, output_location, temp_dir="temp_videos"):
    output_file_path = os.path.join(output_location, "final_video.mp4")  # fixme: later needs to be gcs location
    local_paths = download_from_gcs(gcs_video_urls, temp_dir)

    if not local_paths:
        logging.error("No videos downloaded for merging.")
        return

    list_content = ""
    for path in local_paths:
        absolute_path = os.path.abspath(path)
        formatted_path = absolute_path.replace('\\', '/')
        list_content += f"file '{formatted_path}'\n"

    temp_list_filepath = None
    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', dir=temp_dir) as f:
            temp_list_filepath = f.name
            f.write(list_content)

        logging.info(f"Created temporary file list: {temp_list_filepath}")

        absolute_temp_list_filepath = os.path.abspath(temp_list_filepath)
        formatted_temp_list_filepath = absolute_temp_list_filepath.replace('\\', '/')

        (
            ffmpeg
            .input(formatted_temp_list_filepath, f='concat', safe=0)
            .output(output_file_path, c='copy')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        logging.info(f"Successfully merged videos to {output_file_path} using concat demuxer.")
        # TODO: Add logic to upload to gcs

    except ffmpeg.Error as e:
        logging.error('ffmpeg error:')
        logging.error(e.stdout.decode('utf8'))
        logging.error(e.stderr.decode('utf8'))
        print("An error occurred during ffmpeg processing. Check logs for details.")
        print("This might be because the video streams are not compatible for direct copying.")

    finally:
        if temp_list_filepath and os.path.exists(temp_list_filepath):
            os.remove(temp_list_filepath)
            logging.info(f"Cleaned up temporary file: {temp_list_filepath}")
        for path in local_paths:
            if os.path.exists(path):
                os.remove(path)
                logging.info(f"Cleaned up local file: {path}")
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)
            logging.info(f"Removed temporary directory: {temp_dir}")

    return output_file_path


if __name__ == "__main__":
    # gcs_urls = [
    #     "gs://veo2-exp/dummy/veo2_output_clips_15137911166599222061_sample_0.mp4",
    #     "gs://veo2-exp/dummy/veo2_output_clips_15137911166599222061_sample_1.mp4",
    #     "gs://veo2-exp/dummy/veo2_output_clips_15137911166599222061_sample_2.mp4"
    # ]
    #
    # output_file = "fast_merged_video.mp4"
    #
    # print(f"Attempting to merge videos from GCS: {gcs_urls} into {output_file}")
    # merge_video_clips(gcs_urls, output_file)
    # print("Merging process finished.")

    # output_location = "gs://veo2-exp/dummy/veo2_output_clips"
    # out = generate_video_clip(
    #     prompt="prompt",
    #     output_location=output_location,
    #     aspect_ratio="aspect_ratio",
    #     duration_seconds="duration",
    #     person_generation="person_generation",
    # )
    # import json
    #
    # print(json.dumps(out, indent=3))

    pass
