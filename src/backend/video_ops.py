# src/backend/video_ops.py

import os
import time
import logging
import tempfile
from typing import Union

import ffmpeg
from google import genai
from google.cloud import storage
from google.genai.types import GenerateVideosConfig, Image

from src.backend.utils import load_config, upload_file_to_gcs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()


def generate_video_clip(
        prompt: str,
        output_location: str,
        aspect_ratio: str,
        duration_seconds: int,
        person_generation: str,
        negative_prompt: str = None,
        image_data: Union[str, bytes] = None,
        metadata: dict = None,
):
    """
    Generates video clips using a generative model Veo2.

    Args:
        prompt: Text prompt for video generation.
        output_location: GCS URI for the output directory (e.g., "gs://your-bucket/your-folder").
        aspect_ratio: Video aspect ratio ("16:9" or "9:16").
        duration_seconds: Video duration in seconds (5-8).
        person_generation: Setting for generating people ("allow_adult" or "dont_allow").
        negative_prompt: Optional prompt to discourage content.
        image_data: Optional GCS URI of an image for image-to-video.
        metadata: Optional dictionary for metadata (not used in API call).

    Returns:
        A list of dictionaries, each containing 'gs_uri' and 'http_url'
        for the generated video clips. Empty list if generation fails.
    """

    os.environ["GOOGLE_CLOUD_PROJECT"] = config["project"]["id"]
    os.environ["GOOGLE_CLOUD_LOCATION"] = config["project"]["region"]
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

    if isinstance(image_data, bytes):
        image = Image(image_bytes=image_data, mime_type="image/png")

    elif image_data and image_data.startswith("gs://"):
        image = Image(gcs_uri=image_data, mime_type="image/png")
    else:
        image = None

    requested_number_of_videos = 2

    # Handle duration
    duration_seconds = max(5, min(duration_seconds, 8))

    client = genai.Client(vertexai=True, project=config["project"]["id"], location=config["project"]["location"])
    operation = client.models.generate_videos(
        model=config["veo"]["model_name"],
        image=image,
        prompt=prompt,
        config=GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            output_gcs_uri=output_location,
            number_of_videos=requested_number_of_videos,
            duration_seconds=duration_seconds,
            person_generation=person_generation,
            negative_prompt=negative_prompt,
            enhance_prompt=True,
            seed=None,

        ),
    )

    logger.info("Waiting for operation to complete.")

    while not operation.done:
        time.sleep(10)
        operation = client.operations.get(operation)

    logger.info("Operation Completed!")
    logger.info(f"operation: {operation}")

    generated_clips_data = []
    for video_result_item in operation.result.generated_videos:
        video_uri = video_result_item.video.uri

        parts = video_uri[len("gs://"):].split('/', 1)
        bucket_name = parts[0]
        blob_name = parts[1]
        http_url = f"https://storage.cloud.google.com/{bucket_name}/{blob_name}"

        generated_clips_data.append({
            'gs_uri': video_uri,
            'http_url': http_url
        })
    logger.info(f"Generated clips: {generated_clips_data}")
    return generated_clips_data


def download_from_gcs(gcs_urls, local_dir="temp_videos"):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    storage_client = storage.Client()
    local_paths = []

    for url in gcs_urls:
        if not url.startswith("gs://"):
            logger.error(f"Invalid GCS URL format (expected gs://): {url}")
            continue

        try:
            parts = url[5:].split('/', 1)
            bucket_name = parts[0]
            blob_name = parts[1]

            parent_dir_name = os.path.basename(os.path.dirname(blob_name))
            if not os.path.exists(os.path.join(local_dir, parent_dir_name)):
                os.makedirs(os.path.join(local_dir, parent_dir_name))

            local_filename = os.path.join(local_dir, parent_dir_name, os.path.basename(blob_name))
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.download_to_filename(local_filename)
            local_paths.append(local_filename)
            logger.info(f"Downloaded {url} to {local_filename}")
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")

    return local_paths


def merge_video_clips(gcs_video_urls, output_location, temp_dir="temp_videos"):
    local_paths = download_from_gcs(gcs_video_urls, temp_dir)

    if not local_paths:
        logger.error("No videos downloaded for merging.")
        return

    list_content = ""
    for path in local_paths:
        absolute_path = os.path.abspath(path)
        formatted_path = absolute_path.replace('\\', '/')
        list_content += f"file '{formatted_path}'\n"

    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', dir=temp_dir) as f:
            temp_list_filepath = f.name
            f.write(list_content)

        logger.info(f"Created temporary file list: {temp_list_filepath}")

        absolute_temp_list_filepath = os.path.abspath(temp_list_filepath)
        formatted_temp_list_filepath = absolute_temp_list_filepath.replace('\\', '/')

        with tempfile.NamedTemporaryFile(mode='wb', delete=True, suffix="final_ad.mp4",
                                         dir=temp_dir) as temp_output_file:
            temp_file_path = temp_output_file.name
            (
                ffmpeg
                .input(formatted_temp_list_filepath, f='concat', safe=0)
                .output(temp_file_path, c='copy')
                .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
            )
            logger.info(f"Successfully merged videos to {temp_file_path} using concat demuxer.")

            # Upload to gcs
            with open(temp_file_path, 'rb') as source_file:
                uploaded_file_path = upload_file_to_gcs(file_object=source_file, gcs_destination_path=output_location)

            http_url = uploaded_file_path.replace("gs://", "https://storage.cloud.google.com/")
            return http_url

    except ffmpeg.Error as e:
        logger.error('ffmpeg error:')
        logger.error(e.stdout.decode('utf8'))
        logger.error(e.stderr.decode('utf8'))
        logger.info("An error occurred during ffmpeg processing. Check logs for details.")
        logger.info("This might be because the video streams are not compatible for direct copying.")

    # finally:
    #     if temp_list_filepath and os.path.exists(temp_list_filepath):
    #         os.remove(temp_list_filepath)
    #         logger.info(f"Cleaned up temporary file: {temp_list_filepath}")
    #     for path in local_paths:
    #         if os.path.exists(path):
    #             os.remove(path)
    #             logger.info(f"Cleaned up local file: {path}")
    #     if os.path.exists(temp_dir) and not os.listdir(temp_dir):
    #         os.rmdir(temp_dir)
    #         logger.info(f"Removed temporary directory: {temp_dir}")

    return output_location
