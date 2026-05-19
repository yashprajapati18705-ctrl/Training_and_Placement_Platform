"""Company — Manage Job Postings."""

import streamlit as st
from auth import require_login
from database import (
    get_jobs_by_company, get_job_by_id,
    insert_job, delete_job
)
from database import get_company_by_email


def render():
    require_login('company')
    st.title("💼 Job Postings")

    email        = st.session_state.get('email')
    company      = get_company_by_email(email)
    company_name = company['name'] if company else st.session_state.get('name', '')

    sub = st.session_state.get('company_jobs_sub', 'list')

    if sub == 'list':
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("➕ Post New Job", use_container_width=True):
                st.session_state['company_jobs_sub'] = 'add'
                st.rerun()

        jobs = get_jobs_by_company(company_name)
        if not jobs:
            st.info("You haven't posted any jobs yet.")
            return

        for j in jobs:
            with st.expander(
                f"#{j['id']}  {j['designation']}  |  "
                f"💰 {j['salary_package']}  |  🪑 {j['seats']} seats"
            ):
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"**Min 12th %:** {j['twelfth_percentage'] or '—'}")
                col2.markdown(f"**Min GPA:** {j['grad_gpa'] or '—'}")
                col3.markdown(f"**Experience:** {j['experience'] or '—'}")
                if st.button("🗑 Delete", key=f"dj_{j['id']}", use_container_width=True):
                    delete_job(j['id'])
                    st.success("Job deleted.")
                    st.rerun()

    elif sub == 'add':
        st.subheader("Post a New Job")
        if st.button("← Back to Jobs"):
            st.session_state['company_jobs_sub'] = 'list'
            st.rerun()

        with st.form("post_job_form"):
            designation   = st.text_input("Designation / Role *")
            description   = st.text_area("Job Description")
            experience    = st.text_input("Experience Required (e.g., Fresher, 0-2 years)")
            twelfth_pct   = st.number_input("Minimum 12th Percentage Required", 0.0, 100.0, 60.0, step=0.1)
            grad_gpa      = st.number_input("Minimum Grad GPA Required (0–10)", 0.0, 10.0, 6.0, step=0.01)
            seats         = st.number_input("Number of Seats", 1, 500, 10, step=1)
            salary_package= st.text_input("Salary Package (e.g., 5 LPA)")
            submitted     = st.form_submit_button("Post Job")

        if submitted:
            if not designation:
                st.error("Designation is required.")
            else:
                insert_job({
                    'name':               company_name,
                    'designation':        designation,
                    'description':        description,
                    'experience':         experience,
                    'twelfth_percentage': twelfth_pct,
                    'grad_gpa':           grad_gpa,
                    'seats':              int(seats),
                    'salary_package':     salary_package,
                })
                st.success("Job posted successfully!")
                st.session_state['company_jobs_sub'] = 'list'
                st.rerun()
