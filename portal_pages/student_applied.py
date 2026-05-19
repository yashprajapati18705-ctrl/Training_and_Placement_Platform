"""Student — View Applied Jobs."""

import streamlit as st
from auth import require_login
from database import get_applied_jobs_by_student
from utils import show_table


def render():
    require_login('student')
    st.title("📋 My Applications")
    st.markdown("---")

    email = st.session_state.get('email')
    apps  = get_applied_jobs_by_student(email)

    if not apps:
        st.info("You haven't applied to any job yet.")
        return

    show_table(
        apps,
        columns=['id', 'company_name', 'designation', 'apply_date', 'status']
    )
