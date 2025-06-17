"""Ad Generator"""
import json
import logging

from vertexai.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    SafetySetting,
    GenerationConfig
)

from src.backend.prompts import (generate_script_prompt, generate_veo_compatible_prompt)
from src.backend.utils import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gemini Safety config
safety_config = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
        threshold=HarmBlockThreshold.OFF,
    ),
]


def call_gemini(model, prompt) -> str:
    """Makes an API call to Gemini"""
    logging.info("Making Gemini call")
    response = model.generate_content(prompt)
    return response.text


def get_scene_prompts(ad_idea: str) -> list:
    """
    Calls Gemini to generate a detailed descriptive script for the ad.
    Prompts Gemini to create an elaborate story from a basic ad idea,
    covering visuals, characters, objects, and surroundings for each step.

    Args:
        ad_idea (str): The user-provided ad idea or story.

    Returns:
        list: A scene-wise descriptive ad prompts.
    """
    config = load_config()
    model = GenerativeModel(
        model_name=config["gemini"]["model_name"],
        safety_settings=safety_config,
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            # response_schema=response_schema
        )
    )

    # Generate Ad script
    import time
    t1 = time.time()
    logging.info("Generating Ad script")
    script_prompt = generate_script_prompt(ad_idea=ad_idea, max_scenes=4, ad_duration_sec=15)
    generated_script = call_gemini(model=model, prompt=script_prompt)
    generated_script_json = json.loads(generated_script)
    logging.debug(f"\ngenerated_script_json: \n{json.dumps(generated_script_json)}")
    print("time taken: ", time.time() - t1)

    # TODO: Add last scene consistency logic using image

    # Generate veo compatible prompts
    t2 = time.time()
    logging.info("Generating veo compatible prompts for each scene")
    few_shot_prompts = config["veo"]["prompts"]
    generate_veo_prompts_prompt = generate_veo_compatible_prompt(
        input_script_data=generated_script_json,
        example_prompts=few_shot_prompts)
    generated_veo_prompts = call_gemini(model=model, prompt=generate_veo_prompts_prompt)
    generated_veo_prompts_list = json.loads(generated_veo_prompts)

    for prompt in generated_veo_prompts_list:
        print(prompt)
        print("-" * 100)
    print("time taken: ", time.time() - t2)
    print("total time taken: ", time.time() - t1)

    return generated_veo_prompts_list
