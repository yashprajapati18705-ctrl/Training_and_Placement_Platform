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
