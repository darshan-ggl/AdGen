# src/frontend/vto_page.py

import base64
import logging
import streamlit as st

from src.backend import vto_ops

logger = logging.getLogger(__name__)


def _initialize_vto_session_states():
    """Initializes VTO specific session states if they don't exist."""
    if 'vto_product_image_bytes' not in st.session_state:
        st.session_state['vto_product_image_bytes'] = None
    if 'vto_person_image_bytes' not in st.session_state:
        st.session_state['vto_person_image_bytes'] = None
    if 'vto_result_image_bytes' not in st.session_state:
        st.session_state['vto_result_image_bytes'] = None
    if 'vto_generate_person_ai' not in st.session_state:
        st.session_state['vto_generate_person_ai'] = False
    if 'vto_person_gen_prompt' not in st.session_state:
        st.session_state['vto_person_gen_prompt'] = ""
    if 'vto_generated_videos_data' not in st.session_state:
        st.session_state['vto_generated_videos_data'] = []
    if 'vto_hide_result_image' not in st.session_state:
        st.session_state['vto_hide_result_image'] = False


def _render_scrollable_image(image_bytes, caption: str, height: int = 500):
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    st.markdown(
        f"""
        <div style="height:{height}px; overflow-y:auto; border:1px solid #ccc; padding:4px">
            <img src="data:image/png;base64,{b64}" style="width:100%;" />
            <div style="text-align:center; font-size:smaller; margin-top:4px;">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def _render_vto_header_and_instructions():
    """Renders the header and instructions for the VTO page."""
    # st.header("Virtual Try-On (VTO)")
    # st.subheader("See your product on a generated person and create a video.")

    st.markdown("""
    **Instructions:**
    1.  Upload a **Product Image**.
    2.  Upload a **Person Image**, OR check 'Generate Person Image with AI' and provide a prompt.
    3.  Click 'Perform Virtual Try-On' to see the combined result.
    4.  Click 'Generate Video' to create videos from the VTO result.
    """)


def _handle_product_image_upload():
    """Handles the product image upload and display."""
    st.text("Product Image (Required)")
    uploaded_product_image = st.file_uploader(
        " ",
        type=["png", "jpg", "jpeg"],
        key="vto_product_image_uploader",
        help="Upload the image of the product you want to 'try on'."
    )

    if uploaded_product_image:
        st.session_state['vto_product_image_bytes'] = uploaded_product_image.read()
        _render_scrollable_image(st.session_state['vto_product_image_bytes'], caption="Product Preview")
    else:
        st.session_state['vto_product_image_bytes'] = None


def _handle_person_image_upload_or_generation():
    """Handles person image upload or AI generation logic and display."""
    st.text("Person Image (Optional)")

    current_uploaded_person_image = None
    if not st.session_state['vto_generate_person_ai']:
        current_uploaded_person_image = st.file_uploader(
            " ",
            type=["png", "jpg", "jpeg"],
            key="vto_person_image_uploader",
            help="Upload an image of a person."
        )
        if current_uploaded_person_image:
            st.session_state['vto_person_image_bytes'] = current_uploaded_person_image.read()
        else:
            st.session_state['vto_person_image_bytes'] = None

    st.session_state['vto_generate_person_ai'] = st.checkbox(
        "Generate with AI",
        value=st.session_state['vto_generate_person_ai'],
        key="vto_ai_person_toggle",
        help="Check to have AI generate a person instead of uploading."
    )

    if st.session_state['vto_generate_person_ai']:
        st.session_state['vto_person_gen_prompt'] = st.text_input(
            "Prompt for AI Person",
            value=st.session_state['vto_person_gen_prompt'],
            key="vto_person_gen_prompt_input",
            help="Describe the person for AI generation."
        )
        if st.button("Generate Person", key="vto_trigger_person_gen"):
            if st.session_state['vto_person_gen_prompt']:
                with st.spinner("Generating person image..."):
                    generated_person_bytes = vto_ops.generate_person_image(
                        st.session_state['vto_person_gen_prompt']
                    )
                if generated_person_bytes:
                    st.session_state['vto_person_image_bytes'] = generated_person_bytes
                    st.success("Person generated!")
                else:
                    st.error("Failed to generate person image.")
            else:
                st.warning("Provide a prompt for AI person generation.")

    if st.session_state['vto_person_image_bytes']:
        _render_scrollable_image(st.session_state['vto_person_image_bytes'], caption="Person Preview")
    elif not st.session_state['vto_generate_person_ai'] and current_uploaded_person_image is None:
        st.info("Upload a person image or generate with AI.")


def _render_perform_vto_button():
    """Renders the 'Perform Virtual Try-On' button and result for column layout."""
    st.text("Virtual Try-On")
    st.markdown("")  # Add some spacing

    if st.button("Perform Virtual Try-On", key="vto_perform_button",
                 disabled=st.session_state['vto_product_image_bytes'] is None):
        if st.session_state['vto_product_image_bytes']:
            with st.spinner("Performing Virtual Try-On..."):
                response = vto_ops.perform_virtual_try_on(
                    product_image_bytes=st.session_state['vto_product_image_bytes'],
                    person_image_bytes=st.session_state['vto_person_image_bytes']
                )
                encoded_mask_string = response.predictions[0]["bytesBase64Encoded"]
                vto_result_bytes = base64.b64decode(encoded_mask_string)
            if vto_result_bytes:
                st.session_state['vto_result_image_bytes'] = vto_result_bytes
                st.session_state['vto_generated_videos_data'] = []
                st.session_state['vto_hide_result_image'] = False  # <--- set flag to hide image
            else:
                st.error("Virtual Try-On failed. Check inputs.")
        else:
            st.error("Upload a product image to perform VTO.")

    # Show image only if explicitly allowed
    if st.session_state['vto_result_image_bytes'] and not st.session_state.get('vto_hide_result_image', False):
        _render_scrollable_image(st.session_state['vto_result_image_bytes'], caption="VTO Result")


def _render_vto_result_and_video_generation():
    """Renders only the video generation functionality."""
    if st.session_state['vto_result_image_bytes']:
        st.session_state['vto_hide_result_image'] = True
        st.subheader("Video Generation")

        if st.button("Generate Video", key="vto_generate_video_button"):
            with st.spinner("Generating video from VTO result..."):
                generated_videos_data = vto_ops.generate_vto_video_from_image(
                    image_bytes=st.session_state['vto_result_image_bytes']
                )
            if generated_videos_data:
                st.session_state['vto_generated_videos_data'] = generated_videos_data
                st.success("Video(s) generated!")
            else:
                st.error("Video generation failed.")

        if st.session_state['vto_generated_videos_data']:
            st.subheader("Generated Video(s)")
            videos_per_row = 2
            num_videos = len(st.session_state['vto_generated_videos_data'])

            for i in range(0, num_videos, videos_per_row):
                cols = st.columns(videos_per_row)
                for j in range(videos_per_row):
                    video_index = i + j
                    if video_index < num_videos:
                        with cols[j]:
                            video_item = st.session_state['vto_generated_videos_data'][video_index]
                            if video_item.get('http_url'):
                                st.video(video_item['http_url'], format="video/mp4")
                                st.markdown(f"Clip {video_index + 1}")
                            else:
                                st.warning(f"Clip {video_index + 1} URL not available.")


def render_vto_page():
    """
    Renders the Virtual Try-On (VTO) page with fixed-size columns.
    """
    logger.info("Rendering VTO page.")

    _initialize_vto_session_states()
    FIXED_COLUMN_HEIGHT = 650

    # Add a main container with a border around the entire page content
    with st.container(border=True):
        _render_vto_header_and_instructions()

        col_product_image, col_person_image, col_perform_vto = st.columns(3)
        with col_product_image:
            with st.container(height=FIXED_COLUMN_HEIGHT):
                _handle_product_image_upload()

        with col_person_image:
            with st.container(height=FIXED_COLUMN_HEIGHT):
                _handle_person_image_upload_or_generation()

        with col_perform_vto:
            with st.container(height=FIXED_COLUMN_HEIGHT):
                _render_perform_vto_button()

        with st.container(border=True):
            _render_vto_result_and_video_generation()


if __name__ == '__main__':
    st.set_page_config(layout="centered")
    render_vto_page()
