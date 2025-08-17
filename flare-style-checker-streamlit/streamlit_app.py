import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from processors import process_html, apply_selected_changes

st.set_page_config(page_title="Flare Style Checker", layout="wide")

st.title("Flare Style Checker - MSTP Rules")

if "state" not in st.session_state:
    st.session_state.state = {}

uploaded_file = st.file_uploader(
    "Upload MadCap Flare HTML file", type=["html"], accept_multiple_files=False
)

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    st.session_state.state["original_html"] = content

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Process HTML for MSTP rules & grammar
    edited = process_html(soup)

    st.subheader("Suggested Changes")
    st.write("Review each suggested change. Accept or reject before saving.")

    # Display table with editable 'Accept' column
    edited["Accept"] = True  # Default: accept all
    edited_display = st.data_editor(
        edited,
        use_container_width=True,
        num_rows="dynamic",
    )

    # Store back the edited DataFrame
    st.session_state.state["edited_df"] = edited_display

    # Buttons for actions
    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        st.download_button(
            "Download suggestions (CSV)",
            data=edited_display.to_csv(index=False),
            file_name="suggestions.csv",
            mime="text/csv",
        )

    with col2:
        if st.button("Apply accepted changes and save original file"):
            cleaned_html, changed = apply_selected_changes(soup, edited_display)
            st.session_state.state["cleaned_html"] = cleaned_html
            st.session_state.state["changed"] = changed
            st.success(f"Applied {changed} changes.")

            # Save back to original file path (user input)
            save_path = st.text_input(
                "Enter full path to save the cleaned HTML file",
                value=uploaded_file.name
            )
            if save_path:
                try:
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(cleaned_html)
                    st.success(f"Original file updated: {save_path}")
                except Exception as e:
                    st.error(f"Could not save file: {e}")

    with col3:
        if st.session_state.state.get("cleaned_html"):
            st.download_button(
                "Download cleaned HTML",
                data=st.session_state.state["cleaned_html"],
                file_name=f"cleaned_{uploaded_file.name}",
                mime="text/html",
            )
