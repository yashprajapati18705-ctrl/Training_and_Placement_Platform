"""Student — Upload Academic Info & Resume."""

import streamlit as st
from auth import require_login
from database import get_student_by_email, update_student_academic
from utils import save_resume


def render():
    require_login('student')
    st.title("📤 Upload Academic Info & Resume")
    st.markdown("Fill in your academic details and upload your resume (PDF only).")
    st.markdown("---")

    email   = st.session_state.get('email')
    student = get_student_by_email(email)

    with st.form("upload_form"):
        col1, col2 = st.columns(2)
        with col1:
            tenth_year       = st.number_input("10th Pass Year",  min_value=1990, max_value=2030,
                                               value=int(student['tenth_year'])  if student.get('tenth_year')  else 2018, step=1)
            tenth_pct        = st.number_input("10th Percentage", min_value=0.0,  max_value=100.0,
                                               value=float(student['tenth_percentage']) if student.get('tenth_percentage') else 0.0, step=0.1)
            twelfth_year     = st.number_input("12th Pass Year",  min_value=1990, max_value=2030,
                                               value=int(student['twelfth_year']) if student.get('twelfth_year') else 2020, step=1)
            twelfth_pct      = st.number_input("12th Percentage", min_value=0.0,  max_value=100.0,
                                               value=float(student['twelfth_percentage']) if student.get('twelfth_percentage') else 0.0, step=0.1)
        with col2:
            grad_year        = st.number_input("Graduation Year", min_value=1990, max_value=2030,
                                               value=int(student['grad_year']) if student.get('grad_year') else 2024, step=1)
            grad_gpa         = st.number_input("Graduation GPA (0–10)", min_value=0.0, max_value=10.0,
                                               value=float(student['grad_gpa']) if student.get('grad_gpa') else 0.0, step=0.01)

        uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=['pdf'])
        submitted     = st.form_submit_button("💾 Save Info")

    if submitted:
        resume_path = student.get('resume_path', '') or ''
        if uploaded_file:
            resume_path = save_resume(uploaded_file)

        update_student_academic(email, {
            'tenth_year':        tenth_year,
            'tenth_percentage':  tenth_pct,
            'twelfth_year':      twelfth_year,
            'twelfth_percentage':twelfth_pct,
            'grad_year':         grad_year,
            'grad_gpa':          grad_gpa,
            'resume_path':       resume_path,
        })
        st.success("Academic info updated successfully!")
