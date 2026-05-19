"""Faculty — Selected Students (read-only)."""

import streamlit as st
from auth import require_login
from database import get_all_selected_students
from utils import show_table


def render():
    require_login('faculty')
    st.title("✅ Selected Students")
    st.markdown("All students placed through T&P Cell.")
    st.markdown("---")

    students = get_all_selected_students()
    if not students:
        st.info("No students placed yet.")
        return

    show_table(
        students,
        columns=['id', 'student_name', 'branch', 'company_name', 'role', 'salary']
    )
