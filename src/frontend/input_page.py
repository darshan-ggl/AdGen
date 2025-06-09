# src/frontend/input_page.py

import logging
from typing import Optional, Dict, Any
import time

import streamlit as st
from src.backend import video_ops

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def render_input_page() -> Optional[Dict[str, Any]]:
    """
    Renders the input page for the AI Ad Generator.
    Handles immediate GCS upload of the product image.
    """
    logger.info("Rendering input page...")

    # st.title("✨ AI Ad Generator ✨")
    # st.subheader("Craft your perfect video ad with AI")

    # Use a form to group inputs for potential submission handling
    with st.form(key='ad_input_form'):
        st.header("Ad Content")

        product_ad_idea = st.text_area(
            "Describe your product ad idea",
            help="Provide a detailed description of the scene, actions, and message you want for your ad."
        )

        # Using columns for a horizontal layout for Product Name and Upload Image
        col_name, col_image = st.columns(2)

        with col_name:
            product_name = st.text_input(
                "Product Name (Optional)",
                help="Enter the name of the product being advertised."
            )

        with col_image:
            uploaded_image = st.file_uploader(
                "Upload Product Image (Optional)",
                type=["png", "jpg", "jpeg"],
                help="Upload an image of your product to be potentially included or referenced."
            )

            if uploaded_image is not None and st.session_state.get('last_uploaded_image_id') != uploaded_image.id:
                logger.info(f"New image uploaded: {uploaded_image.name}. Uploading to GCS.")
                with st.spinner("Uploading image to cloud storage..."):
                    timestamp = int(time.time())
                    # image_destination_blob = f"your-ad-generator-bucket/uploaded_images/{timestamp}_{uploaded_image.name}"
                    image_destination_blob = f"mrdarshan-veo-exp/AdGen/Uploaded_Images/{timestamp}_{uploaded_image.name}"

                    gcs_uri = video_ops.upload_streamlit_file_to_gcs(uploaded_image, image_destination_blob)

                    if gcs_uri:
                        st.session_state['uploaded_image_gcs_uri'] = gcs_uri
                        st.session_state[
                            'last_uploaded_image_id'] = uploaded_image.id  # Store ID to prevent re-upload on rerun
                        st.success("Image uploaded to cloud storage!")
                        logger.info(f"Image uploaded to GCS: {gcs_uri}")
                    else:
                        st.session_state['uploaded_image_gcs_uri'] = None
                        st.error("Failed to upload image to cloud storage.")
                        logger.error("Failed to upload product image to GCS.")
                st.rerun()  # Rerun to update the UI with the uploaded image status
            elif uploaded_image is None:
                # If user removes the image, clear the GCS URI from session state
                if 'uploaded_image_gcs_uri' in st.session_state:
                    del st.session_state['uploaded_image_gcs_uri']
                if 'last_uploaded_image_id' in st.session_state:
                    del st.session_state['last_uploaded_image_id']

        st.markdown("---")

        st.header("Video Settings")

        # Using columns for a horizontal layout for core settings
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            aspect_ratio = st.selectbox(
                "Aspect Ratio",
                options=["16:9", "9:16"],
                help="Choose the orientation of the video."
            )

        with col2:
            fps_str = st.selectbox(
                "FPS",
                options=["24"],
                help="Frames per second."
            )
            fps = int(fps_str)

        with col3:
            resolution = st.selectbox(
                "Resolution",
                options=["720p"],
                help="Video resolution."
            )

        with col4:
            person_generation = st.selectbox(
                "Person Generation",
                options=["dont_allow", "allow_adult"],
                help="Control whether people are allowed in the generated video."
            )

        negative_prompt = st.text_area(
            "Negative Prompt (Optional)",
            help="Specify elements you want to avoid in the generated video."
        )
        st.markdown("---")

        _, _, submit_col = st.columns([3, 3, 1])

        with submit_col:
            submit_button = st.form_submit_button(label='Generate Ad Concept')

    # Check if the form was submitted
    if submit_button:
        logger.info("Form submitted. Collecting input data.")
        if not product_ad_idea:
            st.error("Please provide a product ad idea.")
            logger.warning("Form submitted without ad idea.")
            return None  # Return None if required fields are missing

        input_data = {
            "product_ad_idea": product_ad_idea,
            "product_name": product_name,
            "aspect_ratio": aspect_ratio,
            "fps": fps,
            "resolution": resolution,
            "negative_prompt": negative_prompt,
            "person_generation": person_generation,
            "uploaded_image_gcs_uri": st.session_state.get('uploaded_image_gcs_uri', None)
        }
        logger.info("Input data collected and validated.")
        return input_data
    else:
        logger.info("Input page rendered. Waiting for submission.")
        return None


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Input Page Standalone Test")
    collected_data = render_input_page()

    if collected_data:
        st.subheader("Collected Data (for demonstration):")
        st.json(collected_data)
        # In a real app, this is where you'd transition to the next page
        # and pass collected_data to the backend for processing.
