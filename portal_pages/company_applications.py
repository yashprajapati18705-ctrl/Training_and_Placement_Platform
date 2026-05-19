"""Company — Review & Approve/Reject Applications."""

import streamlit as st
from auth import require_login
from database import (
    get_applied_jobs_by_company, get_application_by_id,
    get_student_by_email, approve_application, reject_application,
    get_company_by_email
)
from utils import get_resume_download_button


def render():
    require_login('company')
    st.title("📋 Applications")

    email        = st.session_state.get('email')
    company      = get_company_by_email(email)
    company_name = company['name'] if company else st.session_state.get('name', '')

    sub = st.session_state.get('company_apps_sub', 'list')

    if sub == 'list':
        apps = get_applied_jobs_by_company(company_name)
        if not apps:
            st.info("No applications received yet.")
            return

        st.subheader(f"Total Applications: {len(apps)}")
        for a in apps:
            badge = {"Applied": "🟡", "Rejected": "🔴", "Approved": "🟢"}.get(a['status'], "⚪")
            with st.expander(
                f"{badge} #{a['id']}  {a['student_name']}  —  "
                f"{a['designation']}  |  {a['apply_date']}  |  {a['status']}"
            ):
                if st.button("👁 View Details", key=f"vapp_{a['id']}", use_container_width=True):
                    st.session_state['company_apps_sub'] = 'view'
                    st.session_state['sel_app_id']       = a['id']
                    st.rerun()

    elif sub == 'view':
        aid = st.session_state.get('sel_app_id')
        app = get_application_by_id(aid) if aid else None
        if not app:
            st.error("Application not found.")
            st.session_state['company_apps_sub'] = 'list'
            st.rerun()
            return

        if st.button("← Back to Applications"):
            st.session_state['company_apps_sub'] = 'list'
            st.rerun()

        student = get_student_by_email(app['student_email'])
        st.subheader(f"Application — {app['student_name']}")
        st.markdown(f"**Applied for:** {app['designation']}  |  **Status:** {app['status']}")
        st.markdown("---")

        if student:
            col1, col2 = st.columns(2)
            col1.markdown(f"**Name:** {student['name']}")
            col1.markdown(f"**Email:** {student['email']}")
            col1.markdown(f"**Phone:** {student['phone'] or '—'}")
            col1.markdown(f"**Gender:** {student['gender'] or '—'}")
            col2.markdown(f"**Branch:** {student['branch'] or '—'}")
            col2.markdown(f"**Address:** {student['address'] or '—'}")
            st.markdown("#### Academic Info")
            col3, col4, col5 = st.columns(3)
            col3.markdown(f"**10th Year:** {student['tenth_year'] or '—'}")
            col3.markdown(f"**10th %:** {student['tenth_percentage'] or '—'}")
            col4.markdown(f"**12th Year:** {student['twelfth_year'] or '—'}")
            col4.markdown(f"**12th %:** {student['twelfth_percentage'] or '—'}")
            col5.markdown(f"**Grad Year:** {student['grad_year'] or '—'}")
            col5.markdown(f"**Grad GPA:** {student['grad_gpa'] or '—'}")
            get_resume_download_button(student.get('resume_path', ''))
        else:
            st.warning("Student profile details not found.")

        st.markdown("---")
        if app['status'] == 'Applied':
            col_a, col_r = st.columns(2)
            with col_a:
                if st.button("✅ Approve", use_container_width=True):
                    success = approve_application(aid)
                    if success:
                        st.success("Application approved! Student moved to Selected Students.")
                    else:
                        st.error("Could not approve application.")
                    st.session_state['company_apps_sub'] = 'list'
                    st.rerun()
            with col_r:
                if st.button("❌ Reject", use_container_width=True):
                    reject_application(aid)
                    st.warning("Application rejected.")
                    st.session_state['company_apps_sub'] = 'list'
                    st.rerun()
        else:
            st.info(f"This application has already been **{app['status']}**.")
