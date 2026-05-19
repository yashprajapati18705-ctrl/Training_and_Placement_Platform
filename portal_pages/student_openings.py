"""Student — Browse & Apply to Job Openings."""

import streamlit as st
from auth import require_login
from database import (
    get_all_jobs, get_job_by_id,
    student_already_applied, insert_application,
    get_student_by_email
)


def render():
    require_login('student')
    st.title("💼 Job Openings")

    sub   = st.session_state.get('student_openings_sub', 'list')
    email = st.session_state.get('email')

    if sub == 'list':
        jobs = get_all_jobs()
        if not jobs:
            st.info("No job openings available at the moment.")
            return

        st.subheader(f"Available Openings ({len(jobs)})")
        for j in jobs:
            with st.expander(
                f"**{j['designation']}**  @  {j['name']}  |  "
                f"💰 {j['salary_package']}  |  🪑 {j['seats']} seats"
            ):
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"**Min 12th %:** {j['twelfth_percentage'] or '—'}")
                col2.markdown(f"**Min GPA:** {j['grad_gpa'] or '—'}")
                col3.markdown(f"**Experience:** {j['experience'] or '—'}")
                if st.button("👁 View & Apply", key=f"vaj_{j['id']}"):
                    st.session_state['student_openings_sub'] = 'view'
                    st.session_state['sel_job_id']           = j['id']
                    st.rerun()

    elif sub == 'view':
        jid = st.session_state.get('sel_job_id')
        j   = get_job_by_id(jid) if jid else None
        if not j:
            st.error("Job not found.")
            st.session_state['student_openings_sub'] = 'list'
            st.rerun()
            return

        if st.button("← Back to Openings"):
            st.session_state['student_openings_sub'] = 'list'
            st.rerun()

        st.subheader(f"{j['designation']}  @  {j['name']}")
        col1, col2 = st.columns(2)
        col1.markdown(f"**Salary Package:** {j['salary_package']}")
        col1.markdown(f"**Experience:** {j['experience']}")
        col1.markdown(f"**Seats Available:** {j['seats']}")
        col2.markdown(f"**Min 12th %:** {j['twelfth_percentage']}")
        col2.markdown(f"**Min Grad GPA:** {j['grad_gpa']}")
        st.markdown("**Job Description:**")
        st.write(j['description'] or "No description provided.")
        st.markdown("---")

        # Apply button
        if student_already_applied(email):
            st.warning("⚠️ You have already applied for a job. Only one application is allowed at a time.")
        else:
            if st.button("✅ Apply Now", use_container_width=True):
                student = get_student_by_email(email)
                insert_application({
                    'company_name':  j['name'],
                    'student_name':  student['name'] if student else email,
                    'student_email': email,
                    'designation':   j['designation'],
                })
                st.success(f"Application submitted for **{j['designation']}** at **{j['name']}**!")
                st.rerun()
