"""Admin — Job Openings Management."""

import streamlit as st
from auth import require_login
from database import get_all_jobs, get_job_by_id, insert_job, delete_job, get_all_companies


def render():
    require_login('admin')
    st.title("💼 Job Openings Management")

    sub = st.session_state.get('admin_openings_sub', 'list')

    # ── List ──────────────────────────────────
    if sub == 'list':
        st.subheader("All Job Openings")
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("➕ Add New Opening", use_container_width=True):
                st.session_state['admin_openings_sub'] = 'add'
                st.rerun()

        jobs = get_all_jobs()
        if not jobs:
            st.info("No job openings posted yet.")
            return

        for j in jobs:
            label = f"#{j['id']}  {j['name']}  —  {j['designation']}  |  💰 {j['salary_package'] or '—'}  |  Seats: {j['seats'] or '—'}"
            with st.expander(label):
                st.markdown(f"**Description:** {j['description'] or '—'}")
                st.markdown(f"**Experience:** {j['experience'] or '—'}")
                st.markdown(f"**Min 12th %:** {j['twelfth_percentage'] or '—'}")
                st.markdown(f"**Min Grad GPA:** {j['grad_gpa'] or '—'}")
                if st.button("🗑 Delete Opening", key=f"dj_{j['id']}", use_container_width=False):
                    delete_job(j['id'])
                    st.success(f"Opening '{j['designation']}' at '{j['name']}' deleted.")
                    st.rerun()

    # ── Add ───────────────────────────────────
    elif sub == 'add':
        st.subheader("Post New Job Opening")
        if st.button("← Back to List"):
            st.session_state['admin_openings_sub'] = 'list'
            st.rerun()

        companies = get_all_companies()
        company_names = [c['name'] for c in companies] if companies else []

        with st.form("add_opening_form"):
            if company_names:
                company = st.selectbox("Company *", company_names)
            else:
                st.warning("No companies registered yet. Please add a company first.")
                company = st.text_input("Company Name *")

            designation        = st.text_input("Designation / Role *")
            description        = st.text_area("Job Description")
            experience         = st.text_input("Required Experience (e.g., 0-2 years)")
            twelfth_percentage = st.number_input("Minimum 12th Percentage", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
            grad_gpa           = st.number_input("Minimum Grad GPA", min_value=0.0, max_value=10.0, value=6.0, step=0.1)
            seats              = st.number_input("Number of Seats", min_value=1, value=1, step=1)
            salary_package     = st.text_input("Salary Package (e.g., 4.5 LPA)")
            submitted          = st.form_submit_button("Post Opening")

        if submitted:
            if not company or not designation:
                st.error("Company and Designation are required.")
            else:
                insert_job({
                    'name': company,
                    'designation': designation,
                    'description': description,
                    'experience': experience,
                    'twelfth_percentage': twelfth_percentage,
                    'grad_gpa': grad_gpa,
                    'seats': int(seats),
                    'salary_package': salary_package
                })
                st.success(f"Job opening '{designation}' at '{company}' posted successfully!")
                st.session_state['admin_openings_sub'] = 'list'
                st.rerun()
