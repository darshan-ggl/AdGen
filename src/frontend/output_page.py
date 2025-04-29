# src/frontend/output_page.py
import os
import logging
from typing import List, Dict, Any
import streamlit as st

from src.backend import video_ops

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_scene_state(output_data: List[Dict[str, Any]]):
    """
    Initializes session state for each scene based on output data (prompts/durations).
    """
    if not isinstance(output_data, list):
        logger.error("Attempted to initialize scene state with invalid output_data.")
        st.error("Could not initialize scene data. Please try generating again.")
        if 'scene_states' in st.session_state:
            del st.session_state['scene_states']
        return

    logger.info("Initializing or re-initializing scene states in session state.")
    st.session_state['scene_states'] = []
    for i, scene in enumerate(output_data):
        st.session_state['scene_states'].append({
            'prompt_text': scene.get('prompt', ''),
            'original_prompt': scene.get('prompt', ''),
            'is_edited': False,
            'video_index': 0,
            'confirmed_video_url': None,  # This will store the gs:// URI of the confirmed video
            'is_confirmed': False,
            'gcs_video_paths': [],  # List of dicts {'gs_uri': ..., 'http_url': ...}
            'scene_duration': scene.get('scene_duration', 5)
        })
    if 'regen_count' not in st.session_state:
        st.session_state['regen_count'] = 0
    # Initialize state for back button confirmation
    if 'show_back_confirm' not in st.session_state:
        st.session_state['show_back_confirm'] = False

    logger.info("Scene states initialized.")


def update_prompt_state(scene_index: int):
    """
    Callback function to update prompt text and edited state in session state.
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
    """
    logger.info(f"Scene {scene_index}: Selected video option index {video_option_index}")
    st.session_state['scene_states'][scene_index]['video_index'] = video_option_index


def confirm_video_selection(scene_index: int):
    """
    Callback function to confirm the video selection for a scene.
    """
    scene_state = st.session_state['scene_states'][scene_index]
    selected_index = scene_state.get('video_index', 0)
    gcs_video_data_list = scene_state.get('gcs_video_paths', [])

    if 0 <= selected_index < len(gcs_video_data_list):
        confirmed_video_data = gcs_video_data_list[selected_index]
        confirmed_gs_uri = confirmed_video_data.get('gs_uri')

        if confirmed_gs_uri:
            scene_state['confirmed_video_url'] = confirmed_gs_uri
            scene_state['is_confirmed'] = True
            logger.info(f"Scene {scene_index} video confirmed: {confirmed_gs_uri}")
        else:
            logger.warning(f"Attempted to confirm scene {scene_index} with missing gs_uri.")
            st.warning("Selected video data is incomplete. Cannot confirm.")

    else:
        logger.warning(f"Attempted to confirm scene {scene_index} with invalid video index {selected_index}.")
        st.warning("Please select a valid video before confirming.")


def regenerate_scene_video(scene_index: int):
    """
    Calls the backend video generation function to regenerate video for a specific scene.
    """
    scene_state = st.session_state['scene_states'][scene_index]
    if scene_state.get('is_edited', False):
        edited_prompt = scene_state.get('prompt_text', '')
        duration = scene_state.get('scene_duration', 5)
        ad_input_data = st.session_state.get('ad_input_data', {})
        aspect_ratio = ad_input_data.get('aspect_ratio', '16:9')
        person_generation = ad_input_data.get('person_generation', 'dont_allow')
        image_gcs_uri = None

        logger.info(f"Calling backend to regenerate Scene {scene_index} with prompt: {edited_prompt[:50]}...")

        try:
            output_location = f"gs://veo2-exp/dummy/regenerated_clips/scene_{scene_index}_{st.session_state.get('regen_count', 0)}"
            st.session_state['regen_count'] = st.session_state.get('regen_count', 0) + 1

            with st.spinner(f"Generating new videos for Scene {scene_index + 1}..."):
                generated_clips_data = video_ops.generate_video_clip(
                    prompt=edited_prompt,
                    output_location=output_location,
                    aspect_ratio=aspect_ratio,
                    duration_seconds=duration,
                    person_generation=person_generation,
                    image_gcs_uri=image_gcs_uri
                )
            st.success(f"New videos generated for Scene {scene_index + 1}.")
            logger.info(f"Backend returned new video data for Scene {scene_index}: {generated_clips_data}")

            scene_state['gcs_video_paths'] = generated_clips_data
            scene_state['original_prompt'] = edited_prompt
            scene_state['is_edited'] = False
            scene_state['video_index'] = 0
            scene_state['confirmed_video_url'] = None
            scene_state['is_confirmed'] = False
            st.rerun()

        except Exception as e:
            logger.error(f"Error regenerating video for Scene {scene_index}: {e}")
            st.error(f"Error regenerating video for Scene {scene_index + 1}: {e}")
            scene_state['is_edited'] = False
            st.rerun()


def generate_final_video():
    """
    Collects confirmed video URLs and calls the backend to merge them into a final video.
    """
    logger.info("Initiating final video generation process.")

    scene_states = st.session_state.get('scene_states', [])
    num_scenes = len(scene_states)

    if num_scenes == 0:
        st.warning("No scenes to generate final video.")
        logger.warning("Attempted final generation with no scenes.")
        return

    # Collect confirmed video data
    confirmed_video_data_list = []
    all_scenes_confirmed = True
    for scene_state in scene_states:
        if scene_state.get('is_confirmed', False) and scene_state.get('confirmed_video_url'):
            confirmed_video_data_list.append(
                {'gs_uri': scene_state['confirmed_video_url']})
        else:
            all_scenes_confirmed = False
            break

    if not all_scenes_confirmed:
        st.error("Please confirm all scenes before generating the final video.")
        logger.warning("Final generation attempted with unconfirmed scenes.")
        return

    if not confirmed_video_data_list:
        st.warning("No confirmed scenes with video URLs to merge.")
        logger.warning("Final generation attempted with no confirmed video data.")
        return

    gcs_video_urls = [item['gs_uri'] for item in confirmed_video_data_list]
    logger.info(f"Calling backend to merge videos with gs:// URIs: {gcs_video_urls}")

    try:
        # output_location = f"gs://veo2-exp/dummy/final_ads/ad_{timestamp}"
        output_location = "/Users/mrdarshan/PycharmProjects/AdGen/data/videos/final_video"

        with st.spinner("Merging videos and generating final ad..."):
            # Call merge_video_clips and expect a local file path
            final_video_path = video_ops.merge_video_clips(
                gcs_video_urls=gcs_video_urls,
                output_location=output_location
            )

        # Display the local file path directly
        if final_video_path and os.path.exists(final_video_path):
            st.success("Final video generated!")
            logger.info(f"Final merged video path: {final_video_path}")

            st.subheader("Final Ad Video")
            st.video(final_video_path)

            st.info(f"Video saved locally at: {final_video_path}")

        else:
            st.error("Failed to generate final video locally.")
            logger.error("merge_video_clips did not return a valid local path or file does not exist.")

    except Exception as e:
        logger.error(f"Error during final video generation: {e}")
        st.error(f"An error occurred during final video generation: {e}")


# Helper functions for rendering individual scene components

def _render_scene_header(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the header for a single scene with workflow indicator."""
    indicator_icon = "⏳"
    if scene_state.get('is_edited', False):
        indicator_icon = "✏️"
    if scene_state.get('is_confirmed', False):
        indicator_icon = "✅"
    if not scene_state.get('gcs_video_paths', []):
        indicator_icon = "🔄"

    st.subheader(f"Scene {scene_index + 1} {indicator_icon}")


def _render_video_player_and_selectors(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the video player and clip selection buttons for a single scene."""
    video_data_list = scene_state.get('gcs_video_paths', [])
    num_videos = len(video_data_list)

    if num_videos > 0:
        selected_index = scene_state.get('video_index', 0)
        if not (0 <= selected_index < num_videos):
            selected_index = 0
            if scene_state.get('video_index', 0) != selected_index:
                st.session_state['scene_states'][scene_index]['video_index'] = selected_index
                logger.warning(
                    f"Invalid video index {scene_state.get('video_index', 'N/A')} for scene {scene_index}. Resetting to 0.")

        current_video_data = video_data_list[selected_index]
        current_video_url = current_video_data.get('http_url')

        if current_video_url:
            st.video(current_video_url)
        else:
            st.warning(f"HTTP URL not available for selected video in Scene {scene_index + 1}.")

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
                    disabled=scene_state.get('is_confirmed', False),
                    help=f"View Clip {video_option_index + 1} for Scene {scene_index + 1}"
                )


def _render_prompt_area(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the editable prompt text area for a single scene."""
    edited_prompt_text = st.text_area(
        "Prompt:",
        value=scene_state.get('prompt_text', ''),
        height=150,
        key=f'prompt_area_{scene_index}',
        on_change=update_prompt_state,
        args=(scene_index,),
        disabled=scene_state.get('is_confirmed', False),
        help="Edit the prompt to change the generated video for this scene."
    )
    st.session_state['scene_states'][scene_index]['prompt_text'] = edited_prompt_text


def _render_scene_buttons(scene_index: int, scene_state: Dict[str, Any]):
    """Renders the regenerate and confirm buttons for a single scene."""
    button_col1, button_col2 = st.columns(2)

    is_edited = scene_state.get('is_edited', False)
    is_confirmed = scene_state.get('is_confirmed', False)

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
        output_data (List[Dict[str, Any]]): The list of scene data from the backend,
                                             containing 'prompt' and 'scene_duration'.
    """
    logger.info("Rendering output page with horizontal layout...")

    st.title("🎬 Review and Finalize Your Ad Scenes 🎬")
    st.subheader("Review the generated scenes, edit prompts, and select your preferred videos.")

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

    st.markdown("""
    <style>
    .stButton button {
        margin-right: 5px;
    }
    .st-emotion-cache-1c7y2kw {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    .stButton button[kind="secondary"] {
         margin-left: auto;
         margin-right: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    if ('scene_states' not in st.session_state or
            st.session_state['scene_states'] is None or
            (output_data is not None and len(st.session_state['scene_states']) != len(
                output_data))):
        initialize_scene_state(output_data)

    if 'scene_states' not in st.session_state or st.session_state['scene_states'] is None:
        st.error("Scene data not loaded. Please go back to the input page.")
        return

    scenes_per_row = 3
    scene_data_for_final_generation = []
    num_scenes = len(st.session_state['scene_states'])

    num_confirmed_scenes = sum(1 for scene_state in st.session_state['scene_states'] if
                               scene_state.get('is_confirmed', False))

    for i in range(0, num_scenes, scenes_per_row):
        cols = st.columns(scenes_per_row)

        for j in range(scenes_per_row):
            scene_index = i + j

            if scene_index < num_scenes:
                with cols[j]:
                    scene_state = st.session_state['scene_states'][scene_index]

                    _render_scene_header(scene_index, scene_state)

                    gcs_paths = scene_state.get('gcs_video_paths', [])
                    if len(gcs_paths) > 0:
                        _render_video_player_and_selectors(scene_index, scene_state)
                        _render_prompt_area(scene_index, scene_state)
                        _render_scene_buttons(scene_index, scene_state)

                        if scene_state.get('is_confirmed', False):
                            scene_data_for_final_generation.append({
                                "scene_index": scene_index,
                                "prompt": scene_state.get('prompt_text', ''),
                                "confirmed_video_url": scene_state.get('confirmed_video_url', ''),
                                "scene_duration": scene_state.get('scene_duration', 5)
                            })
                    else:
                        st.video(
                            "https://storage.googleapis.com/gtv-films-clients/veo/dummy/loading.mp4")
                        st.info(f"Generating videos for Scene {scene_index + 1}...")
                        st.text_area(
                            "Prompt:",
                            value=scene_state.get('prompt_text', ''),
                            height=150,
                            key=f'prompt_area_{scene_index}',
                            disabled=True,
                            help="Videos are currently being generated for this scene."
                        )
                        button_col1, button_col2 = st.columns(2)
                        with button_col1:
                            st.button("Re-generate", key=f'regenerate_button_{scene_index}', disabled=True,
                                      help="Wait for initial generation to complete.")
                        with button_col2:
                            st.button("Confirm", key=f'confirm_button_{scene_index}', disabled=True,
                                      help="Wait for initial generation to complete.")

        st.markdown("---")
    st.info(f"Scenes Confirmed: {num_confirmed_scenes}/{num_scenes}")

    all_scenes_confirmed = (num_scenes > 0) and (num_confirmed_scenes == num_scenes)
    _, _, final_button_col = st.columns([3, 3, 1])

    with final_button_col:
        st.button(
            "Generate Final Video",
            key='generate_final_button',
            on_click=generate_final_video,
            disabled=not all_scenes_confirmed,
            help="This button is enabled when all scenes have been confirmed."
        )

    # Add the Back button and confirmation logic at the bottom
    st.markdown("---")  # Separator before back button
    if st.button("← Go Back to Input Page"):
        st.session_state['show_back_confirm'] = True  # Set flag to show confirmation

    # Show confirmation message if flag is set
    if st.session_state.get('show_back_confirm', False):
        st.warning("Going back will discard your current review progress and selections.")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Yes, Go Back", key="confirm_go_back"):
                st.session_state['current_page'] = "Input"  # Assuming page name is "Input" or imported
                # Clear relevant session state data when going back
                st.session_state['ad_input_data'] = None
                st.session_state['output_data'] = None
                st.session_state['scene_states'] = None
                st.session_state['initial_generation_pending'] = False
                st.session_state['show_back_confirm'] = False  # Reset confirmation flag
                st.rerun()
        with col_no:
            if st.button("No, Stay Here", key="cancel_go_back"):
                st.session_state['show_back_confirm'] = False  # Hide confirmation
                st.rerun()
