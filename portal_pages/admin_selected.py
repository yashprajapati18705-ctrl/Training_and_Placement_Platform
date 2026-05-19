"""Admin — Selected (Placed) Students."""

import streamlit as st
from auth import require_login
from database import get_all_selected_students
from utils import show_table


def render():
    require_login('admin')
    st.title("✅ Selected Students")
    st.markdown("List of all placed students across companies.")
    st.markdown("---")

    students = get_all_selected_students()
    if not students:
        st.info("No students have been placed yet.")
        return

    st.subheader(f"Total Placed: {len(students)}")
    show_table(
        students,
        columns=['id', 'student_name', 'branch', 'company_name', 'role', 'salary']
    )
