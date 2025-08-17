# streamlit_app.py
# This is the main Streamlit app for the Flare Style Checker.
# Users can upload a MadCap Flare HTML file, see suggested MSTP & grammar changes,
# accept/reject each suggestion, and save the cleaned HTML back.

import streamlit as st            # Streamlit library to create web apps
import pandas as pd               # Pandas for handling tables of suggestions
from bs4 import BeautifulSoup     # BeautifulSoup to parse HTML

# Import custom functions from processors.py
from processors import process_html, apply_selected_changes

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Flare Style Checker",  # Title shown in browser tab
    layout="wide"                      # Wide layout for better table display
)

st.title("Flare Style Checker - MSTP Rules")

# -------------------------------
# SESSION STATE SETUP
# -------------------------------
# Streamlit resets every run, so we use session_state to store data persistently
if "state" not in st.session_state:
    st.session_state.state = {}  # Dictionary to store uploaded file, suggestions, etc.

# -------------------------------
# FILE UPLOADER
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload MadCap Flare HTML file",   # Label shown above uploader
    type=["html"],                     # Only allow HTML files
    accept_multiple_files=False        # One file at a time
)

# If a file is uploaded
if uploaded_file:
    content = uploaded_file.read().decode("utf-8")  # Read file content as text
    st.session_state.state["original_html"] = content

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Process HTML: check MSTP rules & grammar
    edited = process_html(soup)

    st.subheader("Suggested Changes")
    st.write("Review each suggested change. Accept or reject before saving.")

    # -------------------------------
    # DISPLAY TABLE WITH ACCEPT COLUMN
    # -------------------------------
    edited["apply"] = True  # Default: accept all changes
    edited_display = st.data_editor(
        edited,                  # DataFrame of suggested changes
        use_container_width=True, # Expand table to full width
        num_rows="dynamic",       # Allow dynamic adding/removing rows
    )

    # Store back in session_state
    st.session_state.state["edited_df"] = edited_display

    # -------------------------------
    # BUTTONS FOR DOWNLOAD / SAVE
    # -------------------------------
    col1, col2, col3 = st.columns([1, 1, 1])  # Split screen into 3 columns

    # COLUMN 1: Download suggestions as CSV
    with col1:
        st.download_button(
            "Download suggestions (CSV)",
            data=edited_display.to_csv(index=False),
            file_name="suggestions.csv",
            mime="text/csv",
        )

    # COLUMN 2: Apply changes and save original file
    with col2:
        if st.button("Apply accepted changes and save original file"):
            cleaned_html, changed = apply_selected_changes(soup, edited_display)
            st.session_state.state["cleaned_html"] = cleaned_html
            st.session_state.state["changed"] = changed
            st.success(f"Applied {changed} changes.")

            # Ask user for file path to save cleaned HTML
            save_path = st.text_input(
                "Enter full path to save the cleaned HTML file",
                value=uploaded_file.name  # Default: same name as uploaded
            )
            if save_path:
                try:
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(cleaned_html)
                    st.success(f"Original file updated: {save_path}")
                except Exception as e:
                    st.error(f"Could not save file: {e}")

    # COLUMN 3: Download cleaned HTML
    with col3:
        if st.session_state.state.get("cleaned_html"):
            st.download_button(
                "Download cleaned HTML",
                data=st.session_state.state["cleaned_html"],
                file_name=f"cleaned_{uploaded_file.name}",
                mime="text/html",
            )
