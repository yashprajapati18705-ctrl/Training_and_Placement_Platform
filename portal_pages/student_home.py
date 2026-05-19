"""Student — Home (Profile)."""

import streamlit as st
from auth import require_login
from database import get_student_by_email


def render():
    require_login('student')
    st.title("🎓 My Profile")
    st.markdown("---")

    email   = st.session_state.get('email')
    student = get_student_by_email(email)

    if not student:
        st.error("Profile data not found. Please contact the administrator.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Name:** {student['name']}")
        st.markdown(f"**Email:** {student['email']}")
        st.markdown(f"**Phone:** {student['phone'] or '—'}")
        st.markdown(f"**Gender:** {student['gender'] or '—'}")
        st.markdown(f"**Date of Birth:** {student['dob'] or '—'}")
    with col2:
        st.markdown(f"**Branch:** {student['branch'] or '—'}")
        st.markdown(f"**Address:** {student['address'] or '—'}")

    st.markdown("#### 📚 Academic Info")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown(f"**10th Year:** {student['tenth_year'] or '—'}")
        st.markdown(f"**10th %:** {student['tenth_percentage'] or '—'}")
    with col4:
        st.markdown(f"**12th Year:** {student['twelfth_year'] or '—'}")
        st.markdown(f"**12th %:** {student['twelfth_percentage'] or '—'}")
    with col5:
        st.markdown(f"**Grad Year:** {student['grad_year'] or '—'}")
        st.markdown(f"**Grad GPA:** {student['grad_gpa'] or '—'}")
