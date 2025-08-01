import base64
import timeit
import logging

import vertexai
from google import genai
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import PredictResponse
from google.genai.types import (
    EditImageConfig,
    GenerateImagesConfig,
    Image,
    MaskReferenceConfig,
    MaskReferenceImage,
    RawReferenceImage,
)

from src.backend import video_ops
from src.backend.prompts import person_generation_prompt
from src.backend.utils import load_config

logger = logging.getLogger(__name__)

config = load_config()

PROJECT_ID = config["project"]["id"]
LOCATION = config["project"]["region"]
VTO_MODEL_ENDPOINT = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/virtual-try-on-exp-05-31"

try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    api_regional_endpoint = f"{LOCATION}-aiplatform.googleapis.com"
    client_options = {"api_endpoint": api_regional_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    logger.info(f"[VirtualTryOn Tool] Vertex AI initialized for project:{PROJECT_ID} location:{LOCATION}.")
except Exception as e:
    logger.info(f"[VirtualTryOn Tool ERROR] Failed to initialize Vertex AI client or model endpoint: {e}")
    client = None  # Ensure client is None if init fails


def generate_person_image(user_prompt: str):
    meta_prompt = person_generation_prompt(user_prompt=user_prompt)

    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    generated_prompt = client.models.generate_content(
        model=config["gemini"]["model_name"],
        contents=meta_prompt
    ).text

    response = client.models.generate_images(
        model='imagen-4.0-generate-preview-06-06',
        prompt=generated_prompt,
        config=GenerateImagesConfig(
            number_of_images=1,
        )
    )
    generated_image_bytes = response.generated_images[0].image.image_bytes

    return generated_image_bytes


def perform_virtual_try_on(
        person_image_bytes=None,
        product_image_bytes=None,
        person_image_uri=None,
        product_image_uri=None,
) -> PredictResponse:
    """Constructs a Vertex AI PredictRequest and uses it to call Virtual Try-On."""
    if client is None or VTO_MODEL_ENDPOINT is None:
        raise RuntimeError("Vertex AI client or model endpoint not initialized.")

    try:
        instances = []

        if person_image_uri and product_image_uri:
            instance = {
                "personImage": {"image": {"gcsUri": person_image_uri}},
                "productImages": [{"image": {"gcsUri": product_image_uri}}],
            }
            instances.append(instance)
        elif person_image_bytes and product_image_bytes:
            if isinstance(person_image_bytes, bytes):
                person_image_bytes = base64.b64encode(person_image_bytes).decode('utf-8')
            if isinstance(product_image_bytes, bytes):
                product_image_bytes = base64.b64encode(product_image_bytes).decode('utf-8')

            instance = {
                "personImage": {"image": {"bytesBase64Encoded": person_image_bytes}},
                "productImages": [{"image": {"bytesBase64Encoded": product_image_bytes}}],
            }
            instances.append(instance)
        else:
            raise ValueError(
                "Both person_image_bytes and product_image_bytes or both person_image_uri and product_image_uri must be set"
            )

        start = timeit.default_timer()

        response = client.predict(
            endpoint=VTO_MODEL_ENDPOINT, instances=instances, parameters={}
        )
        end = timeit.default_timer()
        logger.info(f"[Virtual Try-On Core] Try-On took {end - start:.2f}s.")

        return response
    except Exception as e:
        logger.info("Failed to perform VTO. Exception: ", str(e))
        return None


def _generate_background(image_bytes: bytes, prompt: str) -> bytes:
    edit_model = config["imagen"]["edit_model_name"]
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    product_image = Image(
        image_bytes=image_bytes
    )
    raw_ref_image = RawReferenceImage(reference_image=product_image, reference_id=0)
    mask_ref_image = MaskReferenceImage(
        reference_id=1,
        reference_image=None,
        config=MaskReferenceConfig(mask_mode="MASK_MODE_BACKGROUND"),
    )

    edited_image = client.models.edit_image(
        model=edit_model,
        prompt=prompt,
        reference_images=[raw_ref_image, mask_ref_image],
        config=EditImageConfig(
            edit_mode="EDIT_MODE_BGSWAP",
            number_of_images=1,
            seed=1,
            safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
            person_generation="ALLOW_ADULT",
        ),
    )

    final_image = edited_image.generated_images[0].image.image_bytes
    return final_image


def generate_vto_video_from_image(image_bytes: bytes):
    import random
    prompt_lib = [
        """A professional, brightly lit studio background with a seamless white-to-light-grey gradient. The floor is a polished, reflective light grey. No props or distractions, just a clean, expansive space designed to highlight apparel.""",
        """A soft-focus background of a sunlit, modern urban loft. Features include a subtle, textured concrete wall, diffused natural light from large windows, and a hint of warm, unpolished concrete or light wood flooring. Focus on a clean, uncluttered aesthetic with depth, but no distinct objects to distract from the model.""",
        """A softly blurred background depicting a chic, minimalist boutique corner. Elements include a warm, off-white painted wall, a hint of a light oak or beige polished concrete floor, and diffused, warm ambient lighting creating subtle shadows. The focus is on a sophisticated, clean backdrop that complements fashion.""",
        """A subtly blurred outdoor background under overcast natural light, featuring a clean, paved walkway or a smooth, light-colored concrete wall in the distance. The focus is on diffused, even lighting and a neutral, unobtrusive environment that provides depth without drawing attention away from the apparel."""
    ]
    prompt = random.choice(prompt_lib)
    model_with_background_img = _generate_background(image_bytes, prompt)

    # Generate video
    video_prompt = """
        A professional, seamlessly lit studio video featuring a diverse model, gender-neutral, in a full-body shot. The background is a smooth, gradient light gray to off-white wall with a subtle, reflective light gray floor. The camera begins at a medium-wide angle, centered on the model.
        The model performs a single, fluid 360-degree rotation in place, showcasing the garment from all angles – front, sides, and back. Their movement is graceful and natural, allowing the apparel's material and drape to be clearly observed.
        As the model rotates, the camera executes a very subtle, slow counter-rotation, maintaining focus and framing on the model, creating a dynamic yet stable perspective. A brief, soft zoom-in occurs around the 4-second mark to highlight the apparel's texture or a key detail, followed by a gentle zoom-out to return to the full-body view.
        The model maintains a neutral, confident, and approachable expression throughout the clip, with natural eye contact towards the camera at the start and end. Lighting is soft, even, and flattering, emphasizing the apparel's true color and form without harsh shadows. The overall tone is clean, sophisticated, and focused entirely on presenting the garment's aesthetic.
        """

    try:
        output_location = config["veo"]["veo_output_dir"]
        generated_clips_data = video_ops.generate_video_clip(
            prompt=video_prompt,
            output_location=output_location,
            aspect_ratio="9:16",
            duration_seconds=8,
            person_generation="allow_adult",
            image_data=model_with_background_img
        )
        return generated_clips_data
    except Exception as e:
        raise RuntimeError(f"Error generating video: {e}")
