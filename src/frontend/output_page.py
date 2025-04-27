# src/frontend/output_page.py

import streamlit as st
import logging
from typing import List, Dict, Any, Optional
import json  # Import json for pretty printing dummy data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_dummy_output_data() -> List[Dict[str, Any]]:
    """
    Generates dummy data simulating the backend output for video scenes.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a scene
                               with prompt, duration, and GCS video paths.
    """
    logger.info("Generating dummy output data.")
    dummy_data = [
        {
            "prompt": "A close-up shot of a vibrant, juicy apple falling in slow motion into a bowl of water, creating a perfect splash. Studio lighting, high detail.",
            "scene_duration": 5,
            "gcs_video_paths": [
                "https://storage.googleapis.com/gtv-films-clients/veo/b3c920c2-b59c-422a-8537-38d07f42f1e2/videos/f01f5464-a091-47ac-bc5f-b0cc65df649b.mp4",
                "https://storage.googleapis.com/gtv-films-clients/veo/b3c920c2-b59c-422a-8537-38d07f42f1e2/videos/41093f44-b555-45a3-927b-49c6a5c2af1e.mp4"
            ]
        },
        {
            "prompt": "The apple from scene 1 is now sliced and arranged beautifully on a wooden cutting board next to the product packaging. Soft, natural light.",
            "scene_duration": 3,
            "gcs_video_paths": [
                "https://storage.googleapis.com/gtv-films-clients/veo/b3c920c2-b59c-422a-8537-38d07f42f1e2/videos/f2e32376-ca29-428b-912b-69936236c96d.mp4"
            ]
        },
        {
            "prompt": "A hand reaches in to pick up a slice of apple and dips it into a bowl of yogurt. Macro shot focusing on texture and movement.",
            "scene_duration": 4,
            "gcs_video_paths": [
                "https://storage.googleapis.com/gtv-films-clients/veo/b3c920c2-b59c-422a-8537-38d07f42f1e2/videos/c761b7b6-a04b-473e-9b6a-106e2878b2d2.mp4",
                "https://storage.googleapis.com/gtv-films-clients/veo/b3c920c2-b59c-422a-8537-38d07f42f1e2/videos/a9493362-a394-4463-856a-56b334c32ff6.mp4",
                # Added a third video option
                "https://storage.googleapis.com/gtv-films-clients/veo/dummy-regenerated/video_2_v3.mp4"
                # Added another dummy video
            ]
        },
        {
            "prompt": "The product packaging is shown prominently on a clean background with soft focus on the apple slices in the foreground.",
            "scene_duration": 3,
            "gcs_video_paths": [
                "https://storage.googleapis.com/gtv-films-clients/veo/b3c920c2-b59c-422a-8537-38d07f42f1e2/videos/f01f5464-a091-47ac-bc5f-b0cc65df649b.mp4"
                # Reusing a dummy video
            ]
        }
    ]
    return dummy_data


def initialize_scene_state(output_data: List[Dict[str, Any]]):
    """
    Initializes session state for each scene based on output data.

    Args:
        output_data (List[Dict[str, Any]]): The list of scene data from the backend.
    """
    # Check if initialization is needed or if the number of scenes has changed
    if 'scene_states' not in st.session_state or len(st.session_state['scene_states']) != len(output_data):
        logger.info("Initializing or re-initializing scene states in session state.")
        st.session_state['scene_states'] = []
        for i, scene in enumerate(output_data):
            st.session_state['scene_states'].append({
                'prompt_text': scene['prompt'],
                'original_prompt': scene['prompt'],
                'is_edited': False,
                'video_index': 0,  # Start with the first video
                'confirmed_video_url': None,
                'is_confirmed': False,
                'gcs_video_paths': scene['gcs_video_paths'],  # Store paths for easy access
                'scene_duration': scene['scene_duration']  # Store duration as well
            })
    else:
        logger.info("Scene states already initialized.")


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
    # Removed explicit st.rerun() - Streamlit reruns on button click callbacks


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
        # Removed explicit st.rerun() - Streamlit reruns on button click callbacks
    else:
        logger.warning(f"Attempted to confirm scene {scene_index} with invalid video index {selected_index}.")
        st.warning("Please select a valid video before confirming.")


def regenerate_scene_video(scene_index: int):
    """
    Simulates regenerating video for a specific scene based on edited prompt.
    In a real app, this would call the backend API.

    Args:
        scene_index (int): The index of the scene to regenerate.
    """
    scene_state = st.session_state['scene_states'][scene_index]
    if scene_state['is_edited']:
        edited_prompt = scene_state['prompt_text']
        logger.info(f"Simulating regeneration for Scene {scene_index} with prompt: {edited_prompt[:50]}...")
        # --- Call your backend API here with the edited_prompt ---
        # backend_response = your_backend_client.regenerate_video(edited_prompt, scene_state['scene_duration'], ...)

        # --- Simulate receiving new GCS paths (for demonstration) ---
        # Replace this with actual backend call result
        new_gcs_paths = [
            f"https://storage.googleapis.com/gtv-films-clients/veo/dummy-regenerated/video_{scene_index}_v1_{st.session_state.get('regen_count', 0)}.mp4",
            f"https://storage.googleapis.com/gtv-films-clients/veo/dummy-regenerated/video_{scene_index}_v2_{st.session_state.get('regen_count', 0)}.mp4"
            # Simulate different videos on regenerate
        ]
        # Increment a counter to make dummy URLs unique on each regeneration
        st.session_state['regen_count'] = st.session_state.get('regen_count', 0) + 1
        logger.info(f"Simulated new GCS paths received: {new_gcs_paths}")

        # Update scene state with new paths and reset selection/confirmation
        scene_state['gcs_video_paths'] = new_gcs_paths
        scene_state['original_prompt'] = edited_prompt  # New prompt becomes the original
        scene_state['is_edited'] = False  # Reset edited state
        scene_state['video_index'] = 0  # Reset video selection to the first new one
        scene_state['confirmed_video_url'] = None  # Reset confirmation
        scene_state['is_confirmed'] = False
        # Removed explicit st.rerun() - Streamlit reruns on button click callbacks
    else:
        logger.warning(f"Attempted to regenerate Scene {scene_index} without prompt changes.")
        st.warning("Please modify the prompt before regenerating.")


def generate_final_video(final_scene_data: List[Dict[str, Any]]):
    """
    Simulates the final video generation process using confirmed scene data.
    In a real app, this would send the confirmed data to the backend.

    Args:
        final_scene_data (List[Dict[str, Any]]): List of dictionaries, each
                                                 containing confirmed data per scene.
     """
    logger.info("Initiating final video generation with confirmed scenes.")
    # --- Call your backend API here with final_scene_data ---
    logger.info(f"Confirmed data for final generation: {final_scene_data}")
    st.success("Final video generation process initiated (simulated). Check logs.")
    # In a real app, you might show a loading spinner,
    # poll the backend for status, or navigate to a results page.


def _render_scene_header(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the header for a single scene with workflow indicator."""
    indicator_icon = "⏳"  # Pending
    if scene_state['is_edited']:
        indicator_icon = "✏️"  # Edited
    if scene_state['is_confirmed']:
        indicator_icon = "✅"  # Confirmed
    st.subheader(f"Scene {scene_index + 1} {indicator_icon}")  # Add icon to header


def _render_video_player_and_selectors(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the video player and clip selection buttons for a single scene."""
    gcs_paths = scene_state['gcs_video_paths']
    num_videos = len(gcs_paths)

    if num_videos > 0:
        current_video_url = gcs_paths[scene_state['video_index']]
        st.video(current_video_url)

        st.write("Select Clip:")
        video_select_cols = st.columns(num_videos)
        for video_option_index in range(num_videos):
            with video_select_cols[video_option_index]:
                is_selected = (scene_state['video_index'] == video_option_index)
                button_style = "primary" if is_selected else "secondary"
                st.button(
                    f"Clip {video_option_index + 1}",
                    key=f'select_video_{scene_index}_{video_option_index}',
                    on_click=select_video_option,
                    args=(scene_index, video_option_index),
                    type=button_style,
                    disabled=scene_state['is_confirmed'],
                    help=f"View Clip {video_option_index + 1} for Scene {scene_index + 1}"
                )
    else:
        st.warning("No videos generated for this scene.")


def _render_prompt_area(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the editable prompt text area for a single scene."""
    edited_prompt_text = st.text_area(
        "Prompt:",
        value=scene_state['prompt_text'],
        height=150,
        key=f'prompt_area_{scene_index}',
        on_change=update_prompt_state,
        args=(scene_index,),
        disabled=scene_state['is_confirmed'],
        help="Edit the prompt to change the generated video for this scene."
    )
    # Ensure prompt_text in state is updated if text area changed (redundant if on_change works, but safer)
    st.session_state['scene_states'][scene_index]['prompt_text'] = edited_prompt_text


def _render_scene_buttons(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the regenerate and confirm buttons for a single scene."""
    button_col1, button_col2 = st.columns(2)

    with button_col1:
        regen_help_text = "Edit the prompt above to enable regeneration." if not scene_state[
            'is_edited'] else "Generate new videos based on the edited prompt."
        if scene_state['is_confirmed']:
            regen_help_text = "Scene is confirmed, cannot regenerate."
        st.button(
            "Re-generate",
            key=f'regenerate_button_{scene_index}',
            on_click=regenerate_scene_video,
            args=(scene_index,),
            disabled=not scene_state['is_edited'] or scene_state['is_confirmed'],
            help=regen_help_text
        )
    with button_col2:
        confirm_button_label = "Confirmed" if scene_state['is_confirmed'] else "Confirm"
        confirm_help_text = "Confirm your selected video clip for this scene."
        if scene_state['is_confirmed']:
            confirm_help_text = "This scene is confirmed."
        st.button(
            confirm_button_label,
            key=f'confirm_button_{scene_index}',
            on_click=confirm_video_selection,
            args=(scene_index,),
            disabled=scene_state['is_confirmed'],
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

    # Initialize or load scene states from session state
    initialize_scene_state(output_data)

    # Store data for final generation as we iterate and find confirmed scenes
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
                    if len(scene_state['gcs_video_paths']) > 0:
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

        st.markdown("---")  # Add a separator after each row for visual separation

    # Display progress summary
    st.info(f"Scenes Confirmed: {num_confirmed_scenes}/{num_scenes}")

    # Check if all scenes are confirmed *after* iterating through all
    # The count is already calculated above
    all_scenes_confirmed = (num_confirmed_scenes == num_scenes) and (
            num_scenes > 0)  # Ensure there's at least one scene

    # Final Generate Button area
    # Use columns to push the button to the right (adjust ratios as needed)
    _, _, final_button_col = st.columns([3, 3, 1])

    with final_button_col:
        st.button(
            "Generate Final Video",
            key='generate_final_button',
            on_click=generate_final_video,
            args=(scene_data_for_final_generation,),
            disabled=not all_scenes_confirmed,
            help="This button is enabled when all scenes have been confirmed."
        )

    # Optional: Display collected final generation data for debugging
    # if st.button("Show Confirmed Data (Debug)"):
    #      st.json(scene_data_for_final_generation)


if __name__ == '__main__':
    # Example of how to run this page function directly for testing
    st.set_page_config(layout="wide")

    # Get dummy data
    dummy_output = get_dummy_output_data()

    # Render the output page with dummy data
    render_output_page(dummy_output)

    # Example of accessing the final confirmed data after clicking the button (in a real app flow)
    # You would typically check st.session_state['scene_states'] after the
    # generate_final_video function completes or in the next step of your app logic.
