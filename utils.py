"""
utils.py — Shared utilities
Training & Placement Cell Management System
"""

import os
import streamlit as st
import pandas as pd


RESUME_DIR = os.path.join(os.path.dirname(__file__), "uploads", "resumes")
os.makedirs(RESUME_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# Resume helpers
# ─────────────────────────────────────────────

def save_resume(uploaded_file) -> str:
    """Save an uploaded PDF and return the path string."""
    if uploaded_file is None:
        return ""
    filepath = os.path.join(RESUME_DIR, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())
    return filepath


def get_resume_download_button(resume_path: str, label: str = "📄 Download Resume"):
    """Render a download button for a stored resume PDF."""
    if not resume_path or not os.path.exists(resume_path):
        st.info("No resume uploaded.")
        return
    with open(resume_path, "rb") as f:
        st.download_button(
            label=label,
            data=f,
            file_name=os.path.basename(resume_path),
            mime="application/pdf"
        )


# ─────────────────────────────────────────────
# Display helpers
# ─────────────────────────────────────────────

def show_table(rows: list, columns: list | None = None):
    """Render a list of dicts as a styled DataFrame."""
    if not rows:
        st.info("No records found.")
        return
    df = pd.DataFrame(rows)
    if columns:
        df = df[[c for c in columns if c in df.columns]]
    st.dataframe(df, use_container_width=True)


def metric_card(label: str, value: int | str, icon: str = ""):
    """Render a simple metric card inside a column."""
    st.markdown(
        f"""
        <div style="
            background:#f0f2f6;border-radius:12px;
            padding:20px;text-align:center;
            box-shadow:0 2px 6px rgba(0,0,0,0.08)">
          <h2 style="margin:0;color:#1f77b4">{icon} {value}</h2>
          <p style="margin:4px 0 0;color:#555;font-size:14px">{label}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def profile_card(data: dict, title: str = "Profile"):
    """Display a dict of fields in a styled card."""
    st.subheader(title)
    for k, v in data.items():
        if v:
            st.markdown(f"**{k}:** {v}")


# ─────────────────────────────────────────────
# Sidebar navigation helper
# ─────────────────────────────────────────────

def sidebar_nav(items: list[str]) -> str:
    """
    Render sidebar navigation buttons.
    Returns the currently selected page.
    """
    with st.sidebar:
        st.markdown("---")
        for item in items:
            if st.button(item, use_container_width=True, key=f"nav_{item}"):
                st.session_state['page'] = item.lower().replace(" ", "_")
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            from auth import logout
            logout()
            st.rerun()
    return st.session_state.get('page', items[0].lower().replace(" ", "_"))
