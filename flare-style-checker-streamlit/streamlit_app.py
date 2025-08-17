import io
import re
import difflib
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup, NavigableString
from pathlib import Path

from processors import (
    extract_text_nodes,
    apply_mstp_rules_to_nodes,
    apply_langtool_to_nodes,
    apply_selected_changes,
    render_diff_html,
)

st.set_page_config(page_title="Flare Style Checker (Streamlit)", layout="wide")

st.title("Flare Style Checker — Streamlit")
st.caption("Scan MadCap Flare HTML for MSTP + grammar issues, accept/reject changes, and download the cleaned file.")

with st.sidebar:
    st.header("1) Upload")
    uploaded_file = st.file_uploader("Upload a single Flare HTML topic", type=["htm", "html"])
    run_mstp = st.checkbox("Run MSTP rules", value=True)
    run_grammar = st.checkbox("Run Grammar (LanguageTool)", value=True)
    st.markdown("---")
    st.header("Help")
    st.write("Tip: If LanguageTool rate-limits, uncheck Grammar and run MSTP only.")

if "state" not in st.session_state:
    st.session_state.state = {}

if uploaded_file:
    raw = uploaded_file.read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html5lib")  # robust parser for Flare's HTML
    nodes = extract_text_nodes(soup)

    suggestions = []
    if run_mstp:
        suggestions += apply_mstp_rules_to_nodes(nodes)

    if run_grammar:
        try:
            suggestions += apply_langtool_to_nodes(nodes)
        except Exception as e:
            st.warning(f"LanguageTool error: {e}. Continuing with MSTP only.")

    if not suggestions:
        st.success("No suggestions found. 🎉")
    else:
        df = pd.DataFrame(suggestions)
        # Preserve original dataframe for operations
        if "df" not in st.session_state.state:
            st.session_state.state["df"] = df.copy()
        else:
            # keep columns if user edited previously
            common_cols = [c for c in df.columns if c in st.session_state.state["df"].columns]
            st.session_state.state["df"] = df[common_cols]

        st.subheader("Review & accept changes")
        st.write("Toggle **apply** to accept each change. You can filter/sort columns.")
        edited = st.data_editor(
            st.session_state.state["df"],
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "apply": st.column_config.CheckboxColumn("apply"),
                "before": st.column_config.TextColumn("before", width="medium"),
                "after": st.column_config.TextColumn("after", width="medium"),
                "rule_id": st.column_config.TextColumn("rule", width="small"),
                "type": st.column_config.TextColumn("type", width="small"),
            },
            hide_index=True,
        )
        st.session_state.state["df"] = edited

        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.download_button(
                "Download suggestions (CSV)",
                data=edited.to_csv(index=False),
                file_name="suggestions.csv",
                mime="text/csv",
            )
        with col2:
            # Apply and produce cleaned HTML + diff
            if st.button("Apply accepted changes"):
                cleaned_html, changed = apply_selected_changes(soup, edited)
                st.session_state.state["cleaned_html"] = cleaned_html
                st.session_state.state["changed"] = changed
                st.success(f"Applied {changed} changes.")
        with col3:
            if st.session_state.state.get("cleaned_html"):
                st.download_button(
                    "Download cleaned HTML",
                    data=st.session_state.state["cleaned_html"],
                    file_name=f"cleaned_{uploaded_file.name}",
                    mime="text/html",
                )

        if st.session_state.state.get("cleaned_html"):
            st.subheader("Preview: unified diff (first 10k chars)")
            diff_html = render_diff_html(raw, st.session_state.state["cleaned_html"])
            st.components.v1.html(diff_html[:10000], height=400, scrolling=True)

else:
    st.info("Upload a Flare HTML file to begin.")
