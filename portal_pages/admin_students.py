"""Admin — Student Management (CRUD)."""

import streamlit as st
from auth import require_login, hash_password
from database import (
    get_all_students, get_student_by_id,
    insert_student, insert_user, update_student, delete_student, email_exists
)
from utils import show_table, get_resume_download_button


def render():
    require_login('admin')
    st.title("🎓 Students Management")

    sub = st.session_state.get('admin_student_sub', 'list')

    # ── List ──────────────────────────────────
    if sub == 'list':
        st.subheader("All Students")
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("➕ Add New Student", use_container_width=True):
                st.session_state['admin_student_sub'] = 'add'
                st.rerun()

        students = get_all_students()
        if not students:
            st.info("No students registered yet.")
            return

        for s in students:
            with st.expander(f"#{s['id']}  {s['name']}  |  {s['branch']}  |  {s['email']}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("👁 View",   key=f"vs_{s['id']}", use_container_width=True):
                        st.session_state['admin_student_sub'] = 'view'
                        st.session_state['sel_student_id']    = s['id']
                        st.rerun()
                with c2:
                    if st.button("✏️ Edit",  key=f"es_{s['id']}", use_container_width=True):
                        st.session_state['admin_student_sub'] = 'edit'
                        st.session_state['sel_student_id']    = s['id']
                        st.rerun()
                with c3:
                    if st.button("🗑 Delete", key=f"ds_{s['id']}", use_container_width=True):
                        delete_student(s['id'])
                        st.success(f"Student '{s['name']}' deleted.")
                        st.rerun()

    # ── Add ───────────────────────────────────
    elif sub == 'add':
        st.subheader("Add New Student")
        if st.button("← Back to List"):
            st.session_state['admin_student_sub'] = 'list'
            st.rerun()
        with st.form("add_student_form"):
            name     = st.text_input("Full Name *")
            email    = st.text_input("Email *")
            password = st.text_input("Password *", type="password")
            address  = st.text_area("Address")
            gender   = st.selectbox("Gender", ["Male", "Female", "Other"])
            dob      = st.date_input("Date of Birth")
            phone    = st.text_input("Phone")
            branch   = st.text_input("Branch (e.g., Computer Engineering)")
            submitted = st.form_submit_button("Add Student")

        if submitted:
            if not name or not email or not password:
                st.error("Name, Email, and Password are required.")
            elif email_exists(email):
                st.error("Email already registered.")
            else:
                pwd_hash = hash_password(password)
                insert_user(name, email, pwd_hash, 'student')
                insert_student({
                    'name': name, 'address': address, 'gender': gender.lower(),
                    'dob': dob, 'phone': phone, 'branch': branch,
                    'email': email, 'password': pwd_hash
                })
                st.success(f"Student '{name}' added successfully!")
                st.session_state['admin_student_sub'] = 'list'
                st.rerun()

    # ── View ──────────────────────────────────
    elif sub == 'view':
        sid = st.session_state.get('sel_student_id')
        s   = get_student_by_id(sid) if sid else None
        if not s:
            st.error("Student not found.")
            st.session_state['admin_student_sub'] = 'list'
            st.rerun()
            return

        if st.button("← Back to List"):
            st.session_state['admin_student_sub'] = 'list'
            st.rerun()

        st.subheader(f"Student Profile — {s['name']}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** {s['name']}")
            st.markdown(f"**Email:** {s['email']}")
            st.markdown(f"**Phone:** {s['phone'] or '—'}")
            st.markdown(f"**Gender:** {s['gender'] or '—'}")
            st.markdown(f"**DOB:** {s['dob'] or '—'}")
        with col2:
            st.markdown(f"**Branch:** {s['branch'] or '—'}")
            st.markdown(f"**Address:** {s['address'] or '—'}")

        st.markdown("#### Academic Info")
        col3, col4, col5 = st.columns(3)
        with col3:
            st.markdown(f"**10th Year:** {s['tenth_year'] or '—'}")
            st.markdown(f"**10th %:** {s['tenth_percentage'] or '—'}")
        with col4:
            st.markdown(f"**12th Year:** {s['twelfth_year'] or '—'}")
            st.markdown(f"**12th %:** {s['twelfth_percentage'] or '—'}")
        with col5:
            st.markdown(f"**Grad Year:** {s['grad_year'] or '—'}")
            st.markdown(f"**Grad GPA:** {s['grad_gpa'] or '—'}")

        get_resume_download_button(s.get('resume_path', ''))

    # ── Edit ──────────────────────────────────
    elif sub == 'edit':
        sid = st.session_state.get('sel_student_id')
        s   = get_student_by_id(sid) if sid else None
        if not s:
            st.error("Student not found.")
            st.session_state['admin_student_sub'] = 'list'
            st.rerun()
            return

        if st.button("← Back to List"):
            st.session_state['admin_student_sub'] = 'list'
            st.rerun()

        st.subheader(f"Edit Student — {s['name']}")
        with st.form("edit_student_form"):
            name    = st.text_input("Full Name",  value=s['name'])
            address = st.text_area("Address",     value=s['address'] or '')
            gender  = st.selectbox("Gender", ["Male", "Female", "Other"],
                                   index=["male","female","other"].index(
                                       (s['gender'] or 'male').lower()))
            dob     = st.date_input("Date of Birth", value=s['dob'])
            phone   = st.text_input("Phone",  value=s['phone'] or '')
            branch  = st.text_input("Branch", value=s['branch'] or '')
            submitted = st.form_submit_button("Update Student")

        if submitted:
            update_student(sid, {
                'name': name, 'address': address, 'gender': gender.lower(),
                'dob': dob, 'phone': phone, 'branch': branch
            })
            st.success("Student updated successfully!")
            st.session_state['admin_student_sub'] = 'list'
            st.rerun()
