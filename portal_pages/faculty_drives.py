"""Faculty — Placement Drive (read-only job list)."""

import streamlit as st
from auth import require_login
from database import get_all_jobs


def render():
    require_login('faculty')
    st.title("🚀 Placement Drives")
    st.markdown("All active job openings.")
    st.markdown("---")

    jobs = get_all_jobs()
    if not jobs:
        st.info("No placement drives currently active.")
        return

    for j in jobs:
        with st.expander(f"**{j['designation']}**  @  {j['name']}  |  💰 {j['salary_package']}"):
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"**Experience:** {j['experience'] or '—'}")
            col2.markdown(f"**Min 12th %:** {j['twelfth_percentage'] or '—'}")
            col3.markdown(f"**Min GPA:** {j['grad_gpa'] or '—'}")
            st.markdown(f"**Seats:** {j['seats']}")
            st.markdown(f"**Description:** {j['description'] or '—'}")
