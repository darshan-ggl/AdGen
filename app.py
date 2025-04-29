# app.py
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
    """Initializes key session state variables if they don't exist."""
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = INPUT_PAGE
        st.session_state['ad_input_data'] = None
        st.session_state['output_data'] = None  # Stores the initial prompts/durations from ad_generator
        st.session_state['scene_states'] = None  # Stores the mutable state for each scene in the UI
        st.session_state['initial_generation_pending'] = False  # Flag to trigger initial video generation
        logger.info("Initial session state initialized.")


def _handle_input_submission(input_data: dict):
    """Handles actions after the input page form is submitted."""
    if input_data:
        st.session_state['ad_input_data'] = input_data
        logger.info("Input data collected. Transitioning to output page.")
        st.session_state['current_page'] = OUTPUT_PAGE
        st.session_state['output_data'] = None  # Clear previous output data
        st.session_state['scene_states'] = None  # Clear previous scene states
        st.session_state['initial_generation_pending'] = False  # Reset flag
        st.rerun()  # Rerun to switch page


def _generate_initial_prompts():
    """Calls backend to generate initial scene prompts and updates state."""
    logger.info("Generating initial output data (scene prompts) from backend...")
    try:
        ad_idea = st.session_state['ad_input_data'].get('product_ad_idea', '')
        st.session_state['output_data'] = ad_generator.get_scene_prompts(ad_idea=ad_idea)
        logger.info("Initial output data (prompts) generated and stored.")
        st.session_state['initial_generation_pending'] = True  # Set flag to trigger video generation next
        st.rerun()  # Rerun to proceed to initial video generation step
    except Exception as e:
        logger.error(f"Error generating initial output data: {e}")
        st.error(f"An error occurred during ad concept generation: {e}")
        # Reset state and go back to input on error
        st.session_state['current_page'] = INPUT_PAGE
        st.session_state['ad_input_data'] = None
        st.session_state['output_data'] = None
        st.session_state['scene_states'] = None
        st.session_state['initial_generation_pending'] = False
        st.rerun()


def _trigger_initial_video_generation():
    """Triggers initial video generation for all scenes and updates state."""
    logger.info("Initial video generation pending. Triggering generation for all scenes.")
    st.session_state['initial_generation_pending'] = False  # Clear the flag

    # Initialize scene_states based on the output_data (which now has prompts/durations)
    # gcs_video_paths will be empty initially in scene_states
    output_page.initialize_scene_state(st.session_state['output_data'])

    # Trigger video generation for each scene
    # NOTE: This loop contains blocking calls in the current video_ops mock.
    # In a production app, you must handle this asynchronously.
    ad_input_data = st.session_state['ad_input_data']
    aspect_ratio = ad_input_data.get('aspect_ratio', '16:9')
    person_generation = ad_input_data.get('person_generation', 'dont_allow')
    uploaded_image = ad_input_data.get('uploaded_image', None)  # Handle image if needed
    # Note: Handling image upload and getting its GCS URI would be needed here
    # if the backend video generation function actually uses the image.
    # For now, we'll just pass None or a dummy URI if needed by the mock/real function.
    image_gcs_uri = None  # Replace with actual GCS URI if image is uploaded and used

    # Use a placeholder or spinner for the entire generation process
    try:
        with st.spinner("Generating initial video clips for all scenes... This may take a few minutes."):
            for i, scene_state in enumerate(st.session_state['scene_states']):
                prompt = scene_state['prompt_text']
                duration = scene_state['scene_duration']

                # Define output location for initial clips
                output_location = f"gs://veo2-exp/dummy/veo2_output_clips"

                generated_clips_data = video_ops.generate_video_clip(
                    prompt=prompt,
                    output_location=output_location,
                    aspect_ratio=aspect_ratio,
                    duration_seconds=duration,
                    person_generation=person_generation,
                    # image_gcs_uri=... # Pass image GCS URI if applicable
                )
                # Update the scene state with the generated data (list of dicts)
                st.session_state['scene_states'][i]['gcs_video_paths'] = generated_clips_data
                logger.info(f"Initial video data generated for Scene {i}: {generated_clips_data}")

        st.success("Initial video clips generated.")
        st.rerun()  # Rerun to display the output page with videos

    except Exception as e:
        logger.error(f"Error during initial video generation: {e}")
        st.error(f"An error occurred during initial video generation: {e}")
        # Decide how to handle error - maybe clear state and go back to input?
        st.session_state['current_page'] = INPUT_PAGE
        st.session_state['ad_input_data'] = None
        st.session_state['output_data'] = None
        st.session_state['scene_states'] = None
        st.session_state['initial_generation_pending'] = False
        st.rerun()


def _render_output_page_with_data():
    """Renders the output page using data from session state."""
    logger.info("Rendering output page with data and videos.")
    # Pass the output_data (contains initial prompts/durations) to render_output_page.
    # The render function will use scene_states for the current UI state (including video paths).
    output_page.render_output_page(st.session_state['output_data'])


def main():
    """
    Main function to run the Streamlit application.
    Orchestrates page navigation and backend workflow steps.
    """
    _initialize_session_state()
    st.set_page_config(layout="wide", page_title="AI Ad Generator")

    # --- Page Rendering and Logic ---

    if st.session_state['current_page'] == INPUT_PAGE:
        input_data = input_page.render_input_page()
        _handle_input_submission(input_data)

    elif st.session_state['current_page'] == OUTPUT_PAGE:
        # Ensure input data is available to proceed on the output page
        if 'ad_input_data' not in st.session_state or st.session_state['ad_input_data'] is None:
            st.warning("No input data found. Returning to input page.")
            st.session_state['current_page'] = INPUT_PAGE
            st.rerun()
            return  # Stop execution for this run

        # Step 1: Generate Initial Scene Prompts (if not already done)
        if 'output_data' not in st.session_state or st.session_state['output_data'] is None:
            _generate_initial_prompts()
            return  # Stop execution, a rerun is triggered inside _generate_initial_prompts

        # Step 2: Trigger Initial Video Generation (if pending)
        if st.session_state.get('initial_generation_pending', False):
            _trigger_initial_video_generation()
            return  # Stop execution, a rerun is triggered inside _trigger_initial_video_generation

        # Step 3: Render the Output Page (once output_data and initial videos are ready)
        # If we reach here, output_data exists and initial generation is not pending.
        # This means either initial generation finished, or the user is interacting
        # with the output page (editing, regenerating, confirming).
        _render_output_page_with_data()


if __name__ == "__main__":
    main()
