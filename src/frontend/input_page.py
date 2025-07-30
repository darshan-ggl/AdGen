# src/frontend/input_page.py

import logging
from typing import Optional, Dict, Any
import time

import streamlit as st
from src.backend import video_ops
from src.backend.utils import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()


def render_input_page() -> Optional[Dict[str, Any]]:
    """
    Renders the input page for the AI Ad Generator.
    """
    logger.info("Rendering input page...")

    # Dropdown with examples
    examples = [
        "🧪 Try a sample ad idea",
        "Lifestyle sport shoes for the daily commuter. Navigating a bustling city from the subway to the street. Focus on light, quick steps and the shoe's cushioning on hard pavement. Bright, morning light with an energetic, urban feel."
        "Luxury oud and spice perfume. Product showcase on a dark wood surface, caught in a single beam of warm light. Focus on the bottle's heavy glass and gold details. Quiet, rich, and mysterious mood.",
        "Energy drink for gamers and athletes. Dynamic neon-lit action scenes cutting between gaming setup and skateboarding. Dark background with electric blue accents.",
        "Luxury Swiss watch for professionals. Boardroom handshake deals at sunset. Focus on wrist shots during success moments. Gold accents, tailored suit.",
    ]

    # Track current input
    if "ad_text" not in st.session_state:
        st.session_state.ad_text = ""

    # Handle example selection
    def set_example():
        if st.session_state.example != "":
            st.session_state.ad_text = st.session_state.example

    with st.container():
        st.header("Ad Content")

        st.selectbox(
            "Choose a sample (optional)",
            options=examples,
            key="example",
            on_change=set_example,
        )

        product_ad_idea = st.text_area(
            "Describe your product ad idea",
            key="ad_text",
            help="Provide a detailed description of the scene, actions, and message you want for your ad."
        )

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
                options=["allow_adult", "dont_allow"],
                help="Control whether people are allowed in the generated video."
            )

        negative_prompt = st.text_area(
            "Negative Prompt (Optional)",
            help="Specify elements you want to avoid in the generated video."
        )
        _, _, submit_col = st.columns([3, 3, 1])

        with submit_col:
            submit_button = st.button(label='Generate Ad Concept')

    # Check if the form was submitted
    if submit_button:
        logger.info("Form submitted. Collecting input data.")
        if not product_ad_idea:
            st.error("Please provide a product ad idea.")
            logger.warning("Form submitted without ad idea.")
            return None  # Return None if required fields are missing

        input_data = {
            "product_ad_idea": product_ad_idea,
            "aspect_ratio": aspect_ratio,
            "fps": fps,
            "resolution": resolution,
            "negative_prompt": negative_prompt,
            "person_generation": person_generation
        }
        logger.info("Input data collected and validated.")
        return input_data
    else:
        logger.info("Input page rendered. Waiting for submission.")
        return None
