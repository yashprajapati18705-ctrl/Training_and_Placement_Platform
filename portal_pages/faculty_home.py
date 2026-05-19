"""Faculty — Home (Profile)."""

import streamlit as st
from auth import require_login
from database import get_faculty_by_email


def render():
    require_login('faculty')
    st.title("👨‍🏫 My Profile")
    st.markdown("---")

    email   = st.session_state.get('email')
    faculty = get_faculty_by_email(email)

    if not faculty:
        st.error("Profile data not found. Please contact the administrator.")
        return

    st.markdown(f"**Name:** {faculty['name']}")
    st.markdown(f"**Email:** {faculty['email']}")
    st.markdown(f"**Department:** {faculty['department'] or '—'}")
    st.markdown(f"**Phone:** {faculty['phone'] or '—'}")
    st.markdown(f"**Gender:** {faculty['gender'] or '—'}")
    st.markdown(f"**Address:** {faculty['address'] or '—'}")
