"""main"""

import os
import json
from pathlib import Path
import yaml

from vertexai.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    SafetySetting,
    GenerationConfig
)

from src.backend.prompts import (generate_script_prompt, visual_details_and_consistency_prompt,
                                 generate_veo_compatible_prompt)

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


def load_config():
    """
    Loads the configuration from a YAML file located at the project's root.

    Returns:
        dict: The parsed YAML configuration.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        yaml.YAMLError: If there's an error parsing the YAML file.
    """
    # config_file = Path(__file__).parent / "config.yaml"
    config_file = Path(os.getcwd()) / "config.yaml"
    print("Loading config: ", config_file)

    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing config file: {e}")


def call_gemini(model, prompt) -> str:
    """Makes an API call to Gemini"""
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
        model_name=config["llm"]["gemini"]["model_name"],
        safety_settings=safety_config,
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            # response_schema=response_schema
        )
    )

    # Generate Ad script
    script_prompt = generate_script_prompt(ad_idea=ad_idea, max_scenes=4, ad_duration_sec=15)
    generated_script = call_gemini(model=model, prompt=script_prompt)
    generated_script_json = json.loads(generated_script)
    print("\ngenerated_script_json: \n", json.dumps(generated_script_json, indent=3))

    # # Add visual details and element consistency
    # visually_detailed_script_prompt = visual_details_and_consistency_prompt(
    #     script_data=generated_script_json)
    # generated_visually_detailed_script = call_gemini(model=model, prompt=visually_detailed_script_prompt)
    # generated_visually_detailed_script_json = json.loads(generated_visually_detailed_script)
    # print("\ngenerated_visually_detailed_script_json: \n", json.dumps(generated_visually_detailed_script_json, indent=3))

    # TODO: Add last scene consistency logic using image

    # Generate veo compatible prompts
    few_shot_prompts = config["veo"]["prompts"]
    generate_veo_prompts_prompt = generate_veo_compatible_prompt(
        # input_script_data=generated_visually_detailed_script_json,
        input_script_data=generated_script_json,
        example_prompts=few_shot_prompts)
    generated_veo_prompts = call_gemini(model=model, prompt=generate_veo_prompts_prompt)
    generated_veo_prompts_list = json.loads(generated_veo_prompts)

    for prompt in generated_veo_prompts_list:
        print(prompt)
        print("-" * 100)

    return generated_veo_prompts_list


if __name__ == "__main__":
    # input_ad_idea = "A smartwatch ad showing off watch"
    input_ad_idea = "A chips packet ad"

    import time
    st = time.time()
    get_scene_prompts(ad_idea=input_ad_idea)
    print("total_time: ", time.time() - st)
