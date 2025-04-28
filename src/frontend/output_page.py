# src/frontend/output_page.py

import streamlit as st
import logging
import time
from typing import List, Dict, Any, Optional

# Import backend video operations
from src.backend import video_ops

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_scene_state(output_data: List[Dict[str, Any]]):
    """
    Initializes session state for each scene based on output data.
    Called from render_output_page when scene_states needs initialization.

    Args:
        output_data (List[Dict[str, Any]]): The list of scene data from the backend.
    """
    # Check if output_data is valid before proceeding
    if output_data is None or not isinstance(output_data, list):
        logger.error("Attempted to initialize scene state with invalid output_data.")
        st.error("Could not initialize scene data. Please try generating again.")
        # Clear potentially bad state
        if 'scene_states' in st.session_state:
            del st.session_state['scene_states']
        return

    logger.info("Initializing or re-initializing scene states in session state.")
    st.session_state['scene_states'] = []
    for i, scene in enumerate(output_data):
        st.session_state['scene_states'].append({
            'prompt_text': scene.get('prompt', ''),
            'original_prompt': scene.get('prompt', ''),  # Use .get for safety
            'is_edited': False,
            'video_index': 0,  # Start with the first video
            'confirmed_video_url': None,
            'is_confirmed': False,
            'gcs_video_paths': scene.get('gcs_video_paths', []),  # Get paths, default to empty list
            'scene_duration': scene.get('scene_duration', 5)  # Get duration, default to 5s
        })
    # Initialize regen_count if not exists, for dummy video URLs in mock regen
    if 'regen_count' not in st.session_state:
        st.session_state['regen_count'] = 0
    logger.info("Scene states initialized.")


def update_prompt_state(scene_index: int):
    """
    Callback function to update prompt text and edited state in session state.

    Args:
        scene_index (int): The index of the scene being updated.
    """
    current_prompt = st.session_state[f'prompt_area_{scene_index}']
    st.session_state['scene_states'][scene_index]['prompt_text'] = current_prompt
    original_prompt = st.session_state['scene_states'][scene_index]['original_prompt']
    st.session_state['scene_states'][scene_index]['is_edited'] = (current_prompt != original_prompt)
    logger.info(
        f"Scene {scene_index} prompt updated. Edited: {st.session_state['scene_states'][scene_index]['is_edited']}")


def select_video_option(scene_index: int, video_option_index: int):
    """
    Callback function to update the selected video index for a scene.

    Args:
        scene_index (int): The index of the scene being updated.
        video_option_index (int): The index of the video option selected.
    """
    logger.info(f"Scene {scene_index}: Selected video option index {video_option_index}")
    st.session_state['scene_states'][scene_index]['video_index'] = video_option_index
    # Streamlit reruns on button click callbacks


def confirm_video_selection(scene_index: int):
    """
    Callback function to confirm the video selection for a scene.

    Args:
        scene_index (int): The index of the scene being confirmed.
    """
    scene_state = st.session_state['scene_states'][scene_index]
    selected_index = scene_state['video_index']
    if 0 <= selected_index < len(scene_state['gcs_video_paths']):
        confirmed_url = scene_state['gcs_video_paths'][selected_index]
        scene_state['confirmed_video_url'] = confirmed_url
        scene_state['is_confirmed'] = True
        logger.info(f"Scene {scene_index} video confirmed: {confirmed_url}")
        # Streamlit reruns on button click callbacks
    else:
        logger.warning(f"Attempted to confirm scene {scene_index} with invalid video index {selected_index}.")
        st.warning("Please select a valid video before confirming.")


def regenerate_scene_video(scene_index: int):
    """
    Calls the backend video generation function to regenerate video for a specific scene.

    Args:
        scene_index (int): The index of the scene to regenerate.
    """
    scene_state = st.session_state['scene_states'][scene_index]
    if scene_state['is_edited']:
        edited_prompt = scene_state['prompt_text']
        duration = scene_state['scene_duration']
        # Retrieve other necessary inputs from session state or config
        # Assuming aspect_ratio, person_generation are stored in session_state['ad_input_data']
        ad_input_data = st.session_state.get('ad_input_data', {})
        aspect_ratio = ad_input_data.get('aspect_ratio', '16:9')  # Default if not found
        person_generation = ad_input_data.get('person_generation', 'dont_allow')  # Default if not found
        # uploaded_image = ad_input_data.get('uploaded_image', None) # Handle image if needed

        logger.info(f"Calling backend to regenerate Scene {scene_index} with prompt: {edited_prompt[:50]}...")

        # --- Call the actual backend function ---
        # NOTE: This is a blocking call. In production, handle asynchronously.
        try:
            # Define an output location for regenerated clips (e.g., a subfolder per scene)
            # In a real app, this output location logic needs to be robust
            output_location = f"gs://your-ad-generator-bucket/regenerated_clips/scene_{scene_index}_{st.session_state.get('regen_count', 0)}"
            st.session_state['regen_count'] = st.session_state.get('regen_count', 0) + 1  # Increment for unique path

            # Show a spinner or message while generating
            with st.spinner(f"Generating new videos for Scene {scene_index + 1}..."):
                new_gcs_paths = video_ops.generate_video_clip(
                    prompt=edited_prompt,
                    output_location=output_location,
                    aspect_ratio=aspect_ratio,
                    duration_seconds=duration,
                    person_generation=person_generation,
                    # image_gcs_uri=... # Pass image GCS URI if applicable
                )
            st.success(f"New videos generated for Scene {scene_index + 1}.")
            logger.info(f"Backend returned new GCS paths for Scene {scene_index}: {new_gcs_paths}")

            # Update scene state with new paths and reset selection/confirmation
            scene_state['gcs_video_paths'] = new_gcs_paths
            scene_state['original_prompt'] = edited_prompt  # New prompt becomes the original
            scene_state['is_edited'] = False  # Reset edited state
            scene_state['video_index'] = 0  # Reset video selection to the first new one
            scene_state['confirmed_video_url'] = None  # Reset confirmation
            scene_state['is_confirmed'] = False
            st.rerun()  # Rerun to update the UI with new videos and state

        except Exception as e:
            logger.error(f"Error regenerating video for Scene {scene_index}: {e}")
            st.error(f"Error regenerating video for Scene {scene_index + 1}: {e}")
            # Optionally reset state or show error specific to the scene
            scene_state['is_edited'] = False  # Reset edited state on error? Depends on desired behavior.
            st.rerun()  # Rerun to update UI with error message


def generate_final_video():
    """
    Collects confirmed video URLs and calls the backend to merge them into a final video.
    """
    logger.info("Initiating final video generation process.")

    # Collect confirmed data from session state
    final_scene_data = []
    all_scenes_confirmed = True
    num_scenes = len(st.session_state.get('scene_states', []))

    if num_scenes == 0:
        st.warning("No scenes to generate final video.")
        logger.warning("Attempted final generation with no scenes.")
        return

    for i, scene_state in enumerate(st.session_state['scene_states']):
        if scene_state['is_confirmed'] and scene_state['confirmed_video_url']:
            final_scene_data.append({
                "scene_index": i,
                "prompt": scene_state['prompt_text'],
                "confirmed_video_url": scene_state['confirmed_video_url'],
                "scene_duration": scene_state['scene_duration']
            })
        else:
            all_scenes_confirmed = False
            logger.warning(f"Scene {i} is not confirmed or missing confirmed URL.")
            # Break or continue based on whether you want to merge partially confirmed videos

    if not all_scenes_confirmed:
        st.error("Please confirm all scenes before generating the final video.")
        logger.warning("Final generation attempted with unconfirmed scenes.")
        return  # Prevent generation if not all confirmed

    if not final_scene_data:
        st.warning("No confirmed scenes with video URLs to merge.")
        logger.warning("Final generation attempted with no confirmed video data.")
        return

    # Extract just the GCS URLs in the correct order
    # Sort by scene_index to ensure correct order for merging
    final_scene_data.sort(key=lambda x: x['scene_index'])
    gcs_video_urls_to_merge = [item['confirmed_video_url'] for item in final_scene_data]

    logger.info(f"Calling backend to merge videos: {gcs_video_urls_to_merge}")

    # --- Call the actual backend function to merge ---
    # NOTE: This is a blocking call. Handle asynchronously in production.
    try:
        # Define an output location for the final merged video
        # This should be a unique location for each final ad
        # You might use a timestamp or a unique ID
        timestamp = int(time.time())
        output_location = f"gs://your-ad-generator-bucket/final_ads/ad_{timestamp}"

        with st.spinner("Merging videos and generating final ad..."):
            final_video_uri = video_ops.merge_video_clips(
                gcs_video_urls=gcs_video_urls_to_merge,
                output_location=output_location
            )
        st.success("Final video generated!")
        logger.info(f"Final merged video URI: {final_video_uri}")

        # Display the final video or a link to it
        if final_video_uri:
            st.subheader("Final Ad Video")
            st.video(final_video_uri)
            st.markdown(f"Download or share: [Final Video Link]({final_video_uri})")
        else:
            st.error("Failed to generate final video.")

    except Exception as e:
        logger.error(f"Error during final video generation: {e}")
        st.error(f"An error occurred during final video generation: {e}")
        # Optionally update UI state to reflect the error


# Helper functions for rendering individual scene components (moved from main render function)

def _render_scene_header(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the header for a single scene with workflow indicator."""
    indicator_icon = "⏳"  # Pending
    if scene_state.get('is_edited', False):
        indicator_icon = "✏️"  # Edited
    if scene_state.get('is_confirmed', False):
        indicator_icon = "✅"  # Confirmed
    st.subheader(f"Scene {scene_index + 1} {indicator_icon}")  # Add icon to header


def _render_video_player_and_selectors(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the video player and clip selection buttons for a single scene."""
    gcs_paths = scene_state.get('gcs_video_paths', [])  # Use .get with default for safety
    num_videos = len(gcs_paths)

    if num_videos > 0:
        # Ensure the selected video index is valid
        selected_index = scene_state.get('video_index', 0)  # Use .get with default
        if not (0 <= selected_index < num_videos):
            selected_index = 0  # Default to first video if index is invalid
            # Update state only if necessary to avoid unnecessary reruns
            if scene_state.get('video_index', 0) != selected_index:
                st.session_state['scene_states'][scene_index]['video_index'] = selected_index
                logger.warning(
                    f"Invalid video index {scene_state.get('video_index', 'N/A')} for scene {scene_index}. Resetting to 0.")

        current_video_url = gcs_paths[selected_index]
        st.video(current_video_url)

        st.write("Select Clip:")
        video_select_cols = st.columns(num_videos)
        for video_option_index in range(num_videos):
            with video_select_cols[video_option_index]:
                is_selected = (selected_index == video_option_index)
                button_style = "primary" if is_selected else "secondary"
                st.button(
                    f"Clip {video_option_index + 1}",
                    key=f'select_video_{scene_index}_{video_option_index}',
                    on_click=select_video_option,
                    args=(scene_index, video_option_index),
                    type=button_style,
                    disabled=scene_state.get('is_confirmed', False),  # Use .get for safety
                    help=f"View Clip {video_option_index + 1} for Scene {scene_index + 1}"
                )
    # No else block needed here, the calling function checks for empty gcs_video_paths


def _render_prompt_area(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the editable prompt text area for a single scene."""
    edited_prompt_text = st.text_area(
        "Prompt:",
        value=scene_state.get('prompt_text', ''),  # Use .get for safety
        height=150,
        key=f'prompt_area_{scene_index}',
        on_change=update_prompt_state,
        args=(scene_index,),
        disabled=scene_state.get('is_confirmed', False),  # Use .get for safety
        help="Edit the prompt to change the generated video for this scene."
    )
    # Ensure prompt_text in state is updated if text area changed (redundant if on_change works, but safer)
    st.session_state['scene_states'][scene_index]['prompt_text'] = edited_prompt_text


def _render_scene_buttons(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the regenerate and confirm buttons for a single scene."""
    # Use columns within the container to attempt alignment
    button_col1, button_col2 = st.columns(2)

    is_edited = scene_state.get('is_edited', False)  # Use .get for safety
    is_confirmed = scene_state.get('is_confirmed', False)  # Use .get for safety

    with button_col1:
        regen_help_text = "Edit the prompt above to enable regeneration." if not is_edited else "Generate new videos based on the edited prompt."
        if is_confirmed:
            regen_help_text = "Scene is confirmed, cannot regenerate."
        st.button(
            "Re-generate",
            key=f'regenerate_button_{scene_index}',
            on_click=regenerate_scene_video,
            args=(scene_index,),
            disabled=not is_edited or is_confirmed,
            help=regen_help_text
        )
    with button_col2:
        confirm_button_label = "Confirmed" if is_confirmed else "Confirm"
        confirm_help_text = "Confirm your selected video clip for this scene."
        if is_confirmed:
            confirm_help_text = "This scene is confirmed."
        st.button(
            confirm_button_label,
            key=f'confirm_button_{scene_index}',
            on_click=confirm_video_selection,
            args=(scene_index,),
            disabled=is_confirmed,
            help=confirm_help_text
        )


def render_output_page(output_data: List[Dict[str, Any]]):
    """
    Renders the output page displaying generated scenes and controls with horizontal layout.

    Args:
        output_data (List[Dict[str, Any]]): The list of scene data from the backend.
    """
    logger.info("Rendering output page with horizontal layout...")

    st.title("🎬 Review and Finalize Your Ad Scenes 🎬")
    st.subheader("Review the generated scenes, edit prompts, and select your preferred videos.")

    # Add explicit instructions at the top
    st.markdown("""
    **Instructions:**
    1.  Review each scene below.
    2.  Watch the different video clips generated for each scene using the 'Select Clip' buttons.
    3.  (Optional) Edit the prompt below the video if you want to change the scene.
    4.  If you edited the prompt, click 'Re-generate' to get new video options based on your changes.
    5.  Click 'Confirm' for your chosen clip once you are satisfied with the video and prompt for that scene.
    6.  Repeat for all scenes.
    7.  Once all scenes are confirmed (indicated by the 'Confirmed' button and checkmark icon), the 'Generate Final Video' button will be enabled.
    """, unsafe_allow_html=True)

    # Inject CSS for button alignment
    st.markdown("""
    <style>
    /* Style for the video selection buttons */
    .stButton button {
        margin-right: 5px; /* Space between buttons */
    }
     /* Attempt to align buttons within their column */
    .st-emotion-cache-1c7y2kw { /* Target the specific column container class - Note: This class name can be unstable across Streamlit versions */
        display: flex;
        flex-direction: column;
        align-items: flex-end; /* Align items to the right within the column */
    }
     /* Adjust alignment for the regenerate button specifically if needed */
    .stButton button[kind="secondary"] { /* Target secondary buttons (like Re-generate) */
         margin-left: auto; /* Push to the right */
         margin-right: 0; /* Remove default right margin */
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize or load scene states from session state based on the passed output_data
    # This ensures scene_states is in sync with the output_data received from the backend
    if ('scene_states' not in st.session_state or
            st.session_state['scene_states'] is None or
            len(st.session_state['scene_states']) != len(output_data)):  # Re-initialize if data length changes
        initialize_scene_state(output_data)

    # Ensure scene_states exists in session state after potential initialization
    if 'scene_states' not in st.session_state or st.session_state['scene_states'] is None:
        st.error("Scene data not loaded. Please go back to the input page.")
        # Optionally add a button to go back
        # if st.button("Go to Input Page"):
        #    st.session_state['current_page'] = INPUT_PAGE
        #    st.rerun()
        return  # Stop rendering if data is missing

    # Store data for final generation as we iterate and find confirmed scenes
    # This list is built dynamically during rendering to pass to the final generate function
    scene_data_for_final_generation = []

    scenes_per_row = 3  # Define how many scenes per row

    # Iterate through scenes and group them into rows
    num_scenes = len(st.session_state['scene_states'])

    # Calculate confirmed scenes count for progress summary
    num_confirmed_scenes = sum(1 for scene_state in st.session_state['scene_states'] if scene_state['is_confirmed'])

    for i in range(0, num_scenes, scenes_per_row):
        # Create columns for the current row
        cols = st.columns(scenes_per_row)

        # Iterate through the scenes that belong in this row
        for j in range(scenes_per_row):
            scene_index = i + j  # Calculate the actual index of the scene

            # Check if this scene index is within the bounds of the total number of scenes
            if scene_index < num_scenes:
                # Place content for this scene in the j-th column of the current row
                with cols[j]:
                    scene_state = st.session_state['scene_states'][scene_index]

                    # Render scene components using modular functions
                    _render_scene_header(scene_index, scene_state)
                    _render_video_player_and_selectors(scene_index, scene_state)

                    # Check if videos exist before rendering prompt and buttons
                    if len(scene_state.get('gcs_video_paths', [])) > 0:  # Use .get for safety
                        _render_prompt_area(scene_index, scene_state)
                        _render_scene_buttons(scene_index, scene_state)

                        # Store confirmed URL for final generation if confirmed
                        if scene_state['is_confirmed']:
                            scene_data_for_final_generation.append({
                                "scene_index": scene_index,
                                "prompt": scene_state['prompt_text'],
                                "confirmed_video_url": scene_state['confirmed_video_url'],
                                "scene_duration": scene_state['scene_duration']
                            })
                    else:
                        st.warning("No videos generated for this scene.")
                        # If no videos, this scene cannot be confirmed for final generation
                        # This scene will not be included in final_scene_data, affecting all_scenes_confirmed check

        st.markdown("---")  # Add a separator after each row for visual separation

    # Display progress summary
    st.info(f"Scenes Confirmed: {num_confirmed_scenes}/{num_scenes}")

    # Check if all scenes are confirmed *after* iterating through all
    # The count is already calculated above
    # Also check that the number of confirmed scenes matches the total number of scenes
    all_scenes_confirmed = (num_scenes > 0) and (num_confirmed_scenes == num_scenes)

    # Final Generate Button area
    # Use columns to push the button to the right (adjust ratios as needed)
    _, _, final_button_col = st.columns([3, 3, 1])

    with final_button_col:
        st.button(
            "Generate Final Video",
            key='generate_final_button',
            on_click=generate_final_video,  # Call the function directly
            # args=(scene_data_for_final_generation,), # No need to pass args if function reads from session state
            disabled=not all_scenes_confirmed,
            help="This button is enabled when all scenes have been confirmed."
        )

    # Optional: Display collected final generation data for debugging
    # if st.button("Show Confirmed Data (Debug)"):
    #      st.json(scene_data_for_final_generation)
