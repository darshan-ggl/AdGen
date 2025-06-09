# src/app.py

import sys
import logging
from pathlib import Path
import streamlit as st
from src.backend import ad_generator
from src.backend import video_ops
from src.frontend import input_page, output_page

# Set up logging for the main app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the project root is in the path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Define page names
INPUT_PAGE = "Input"
OUTPUT_PAGE = "Output"


def _initialize_session_state():
    """Initializes key session state variables."""
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = INPUT_PAGE
        st.session_state['ad_input_data'] = None
        st.session_state['output_data'] = None
        st.session_state['scene_states'] = None
        st.session_state['initial_generation_pending'] = False
        # Initialize tab state if needed, default to 'Quick AdGen'
        if 'active_tab' not in st.session_state:
            st.session_state['active_tab'] = "Quick AdGen"
        logger.info("Initial session state initialized.")


def _handle_input_submission(input_data: dict):
    """Handles actions after the input page form is submitted."""
    if input_data:
        st.session_state['ad_input_data'] = input_data
        logger.info("Input data collected. Transitioning to output page.")
        st.session_state['current_page'] = OUTPUT_PAGE
        st.session_state['output_data'] = None
        st.session_state['scene_states'] = None
        st.session_state['initial_generation_pending'] = False
        st.rerun()


def _generate_initial_prompts():
    """Calls backend to generate initial scene prompts."""
    logger.info("Generating initial output data (scene prompts) from backend...")
    try:
        ad_idea = st.session_state['ad_input_data'].get('product_ad_idea', '')
        st.session_state['output_data'] = ad_generator.get_scene_prompts(ad_idea=ad_idea)
        logger.info("Initial output data (prompts) generated and stored.")
        st.session_state['initial_generation_pending'] = True
        st.rerun()
    except Exception as e:
        logger.error(f"Error generating initial output data: {e}")
        st.error(f"An error occurred during ad concept generation: {e}")
        st.session_state['current_page'] = INPUT_PAGE
        st.session_state['ad_input_data'] = None
        st.session_state['output_data'] = None
        st.session_state['scene_states'] = None
        st.session_state['initial_generation_pending'] = False
        st.rerun()


def _trigger_initial_video_generation():
    """Triggers initial video generation for all scenes."""
    logger.info("Initial video generation pending. Triggering generation for all scenes.")
    st.session_state['initial_generation_pending'] = False

    output_page.initialize_scene_state(st.session_state['output_data'])

    ad_input_data = st.session_state['ad_input_data']
    aspect_ratio = ad_input_data.get('aspect_ratio', '16:9')
    person_generation = ad_input_data.get('person_generation', 'dont_allow')
    uploaded_image = ad_input_data.get('uploaded_image', None)
    product_name = ad_input_data.get('product_name', '')
    negative_prompt = ad_input_data.get('negative_prompt', '')

    image_gcs_uri = None
    if uploaded_image:
        logger.info(f"Uploaded image detected: {uploaded_image.name}. Uploading to GCS.")
        image_destination_blob = f"your-ad-generator-bucket/uploaded_images/{uploaded_image.name}"
        image_gcs_uri = video_ops.upload_streamlit_file_to_gcs(uploaded_image, image_destination_blob)
        if image_gcs_uri:
            logger.info(f"Image uploaded to GCS: {image_gcs_uri}")
        else:
            logger.error("Failed to upload image to GCS.")
            st.error("Failed to upload product image. Video generation may be affected.")

    metadata = {'product_name': product_name} if product_name else None

    try:
        with st.spinner("Generating initial video clips for all scenes... This may take a few minutes."):
            for i, scene_state in enumerate(st.session_state['scene_states']):
                prompt = scene_state['prompt_text']
                duration = scene_state['scene_duration']

                # Define output location for initial clips
                output_location = f"gs://veo2-exp/dummy/veo2_output_clips"
                # output_location = "gs://mrdarshan-veo-exp/veo2_output_clips/AdGen"

                generated_clips_data = video_ops.generate_video_clip(
                    prompt=prompt,
                    output_location=output_location,
                    aspect_ratio=aspect_ratio,
                    duration_seconds=duration,
                    person_generation=person_generation,
                    metadata=metadata,
                    negative_prompt=negative_prompt,
                    image_gcs_uri=image_gcs_uri
                )
                st.session_state['scene_states'][i]['gcs_video_paths'] = generated_clips_data
                logger.info(f"Initial video data generated for Scene {i}: {generated_clips_data}")

        st.success("Initial video clips generated.")
        st.rerun()

    except Exception as e:
        logger.error(f"Error during initial video generation: {e}")
        st.error(f"An error occurred during initial video generation: {e}")
        st.session_state['current_page'] = INPUT_PAGE
        st.session_state['ad_input_data'] = None
        st.session_state['output_data'] = None
        st.session_state['scene_states'] = None
        st.session_state['initial_generation_pending'] = False
        st.rerun()


def _render_quick_adgen_tab():
    """Renders the content for the 'Quick AdGen' tab."""
    if st.session_state['current_page'] == INPUT_PAGE:
        input_data = input_page.render_input_page()
        _handle_input_submission(input_data)

    elif st.session_state['current_page'] == OUTPUT_PAGE:
        if 'ad_input_data' not in st.session_state or st.session_state['ad_input_data'] is None:
            st.warning("No input data found. Returning to input page.")
            st.session_state['current_page'] = INPUT_PAGE
            st.rerun()
            return

        if 'output_data' not in st.session_state or st.session_state['output_data'] is None:
            _generate_initial_prompts()
            return

        if st.session_state.get('initial_generation_pending', False):
            _trigger_initial_video_generation()
            return

        logger.info("Rendering output page with data and videos.")
        output_page.render_output_page(st.session_state['output_data'])


def _render_product_adgen_tab():
    """Renders the content for the 'Product AdGen' tab."""
    st.info("This tab is under construction. Future features for product-centric ad generation will appear here!")


def main():
    """
    Main function to run the Streamlit application.
    Orchestrates page navigation and backend workflow steps within tabs.
    """
    _initialize_session_state()
    st.set_page_config(layout="wide", page_title="AI Ad Generator")  # Page config for browser tab title

    # Main application title and subheader, placed before tabs
    st.title("✨ AI Ad Generator ✨")
    st.subheader("Craft your perfect video ad with AI")

    # Create tabs
    tab_quick_adgen, tab_product_adgen = st.tabs(["Quick AdGen", "Product AdGen"])

    with tab_quick_adgen:
        _render_quick_adgen_tab()

    with tab_product_adgen:
        _render_product_adgen_tab()


if __name__ == "__main__":
    main()
