import logging
import traceback
import streamlit as st

from src.frontend import input_page, output_page

# Set up logging for the main app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define page names
INPUT_PAGE = "Input"
OUTPUT_PAGE = "Output"


def main():
    """
    Main function to run the Streamlit application.
    Handles page navigation based on session state.
    """
    st.set_page_config(layout="wide", page_title="AI Ad Generator")
    logger.info("Starting Streamlit app.")

    # Initialize session state for page navigation and data storage
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = INPUT_PAGE
        logger.info(f"Initial page set to: {st.session_state['current_page']}")

    # Render the current page
    if st.session_state['current_page'] == INPUT_PAGE:
        # The input page returns data if the form is submitted
        input_data = input_page.render_input_page()
        if input_data:
            # Store input data in session state
            st.session_state['ad_input_data'] = input_data
            logger.info("Input data collected. Attempting to generate scene prompts.")
            # Transition to a loading state or directly to output page logic
            # In a real app, you might show a spinner here while calling the backend
            st.session_state[
                'current_page'] = OUTPUT_PAGE  # Assume successful backend call will happen before rendering output
            st.session_state['output_data'] = None  # Clear previous output data
            st.session_state['scene_states'] = None  # Clear previous scene states
            st.rerun()  # Rerun the app to switch page

    elif st.session_state['current_page'] == OUTPUT_PAGE:
        # The output page requires generated data
        # This is where we would typically call the backend to get the initial output_data
        # For demonstration, we'll call the backend logic here if data isn't already present

        if 'ad_input_data' not in st.session_state or st.session_state['ad_input_data'] is None:
            st.warning("No input data found. Returning to input page.")
            st.session_state['current_page'] = INPUT_PAGE
            st.rerun()
            return  # Stop execution for this run

        # Check if output data is already generated (e.g., after initial prompt generation)
        if 'output_data' not in st.session_state or st.session_state['output_data'] is None:
            logger.info("Generating initial output data from backend...")
            try:
                # Call the backend function to get initial scene prompts
                from src.backend.ad_generator import get_scene_prompts

                ad_idea = st.session_state['ad_input_data'].get('product_ad_idea', '')

                # You might pass other relevant inputs like product name, image etc.
                st.session_state['output_data'] = get_scene_prompts(ad_idea=ad_idea)
                logger.info("Initial output data generated and stored in session state.")

                # # Re-initialize scene states based on the new output data
                # output_page.initialize_scene_state(st.session_state['output_data'])
                st.rerun()  # Rerun to display the output page with data
                return  # Stop execution for this run
            except Exception as e:
                logger.error(f"Error generating initial output data: {e}")
                print(traceback.format_exc())
                st.error(f"An error occurred during ad concept generation: {e}")
                st.session_state['current_page'] = INPUT_PAGE  # Go back to input on error
                st.rerun()
                return  # Stop execution for this run

        # If output data exists, render the output page
        logger.info("Rendering output page with existing data.")
        output_page.render_output_page(st.session_state['output_data'])

    # Add a button to navigate back to the input page (optional, for testing)
    # This could also be a sidebar link in a multi-page app structure
    # if st.session_state['current_page'] == OUTPUT_PAGE:
    #     if st.button("← Go Back to Input"):
    #         st.session_state['current_page'] = INPUT_PAGE
    #         # Clear relevant session state data when going back
    #         st.session_state['ad_input_data'] = None
    #         st.session_state['output_data'] = None
    #         st.session_state['scene_states'] = None
    #         st.rerun()


if __name__ == "__main__":
    main()
