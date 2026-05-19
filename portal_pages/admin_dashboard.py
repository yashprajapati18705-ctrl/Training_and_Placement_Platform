"""Admin — College Info management."""

import streamlit as st
from auth import require_login
from database import get_college_info, update_college_info


def render():
    require_login('admin')
    st.title("🏛️ College Information")

    info = get_college_info()
    fields = [
        "College Name", "Address", "Contact", "Email", "Website", "Established"
    ]

    with st.form("college_info_form"):
        values = {}
        for field in fields:
            values[field] = st.text_input(field, value=info.get(field, ''))
        submitted = st.form_submit_button("💾 Save Changes")

    if submitted:
        update_college_info(values)
        st.success("College information updated successfully!")
"""Admin — Dashboard with summary counts."""

import streamlit as st
from auth import require_login
from database import get_dashboard_counts, get_college_info


def render():
    require_login('admin')
    st.title("🏠 Admin Dashboard")

    info = get_college_info()
    college_name = info.get("College Name", "Training & Placement Cell")
    st.markdown(f"### Welcome to {college_name}")
    st.markdown("---")

    counts = get_dashboard_counts()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎓 Students", counts.get("students", 0))
    with col2:
        st.metric("👨‍🏫 Faculty", counts.get("faculties", 0))
    with col3:
        st.metric("🏢 Companies", counts.get("companies", 0))
    with col4:
        st.metric("✅ Selected", counts.get("selected_students", 0))

    st.markdown("---")
    st.info("Use the sidebar menu to manage students, faculty, companies, job openings, and more.")
