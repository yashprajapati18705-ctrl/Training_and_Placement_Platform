"""Faculty — Browse Students (View + Add + Edit)."""

import streamlit as st
from auth import require_login, hash_password
from database import (
    get_all_students, get_student_by_id,
    insert_student, insert_user, update_student, email_exists
)
from utils import get_resume_download_button


def render():
    require_login('faculty')
    st.title("🎓 Students")

    sub = st.session_state.get('faculty_student_sub', 'list')

    if sub == 'list':
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("➕ Add Student", use_container_width=True):
                st.session_state['faculty_student_sub'] = 'add'
                st.rerun()

        students = get_all_students()
        if not students:
            st.info("No students registered yet.")
            return

        for s in students:
            with st.expander(f"#{s['id']}  {s['name']}  |  {s['branch']}  |  {s['email']}"):
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("👁 View", key=f"fvs_{s['id']}", use_container_width=True):
                        st.session_state['faculty_student_sub'] = 'view'
                        st.session_state['sel_student_id']      = s['id']
                        st.rerun()
                with c2:
                    if st.button("✏️ Edit", key=f"fes_{s['id']}", use_container_width=True):
                        st.session_state['faculty_student_sub'] = 'edit'
                        st.session_state['sel_student_id']      = s['id']
                        st.rerun()

    elif sub == 'view':
        sid = st.session_state.get('sel_student_id')
        s   = get_student_by_id(sid) if sid else None
        if not s:
            st.error("Student not found.")
            st.session_state['faculty_student_sub'] = 'list'
            st.rerun()
            return
        if st.button("← Back"):
            st.session_state['faculty_student_sub'] = 'list'
            st.rerun()
        st.subheader(f"Student Profile — {s['name']}")
        col1, col2 = st.columns(2)
        col1.markdown(f"**Name:** {s['name']}")
        col1.markdown(f"**Email:** {s['email']}")
        col1.markdown(f"**Phone:** {s['phone'] or '—'}")
        col1.markdown(f"**Gender:** {s['gender'] or '—'}")
        col1.markdown(f"**DOB:** {s['dob'] or '—'}")
        col2.markdown(f"**Branch:** {s['branch'] or '—'}")
        col2.markdown(f"**Address:** {s['address'] or '—'}")
        st.markdown("#### Academic Info")
        col3, col4, col5 = st.columns(3)
        col3.markdown(f"**10th Year:** {s['tenth_year'] or '—'}")
        col3.markdown(f"**10th %:** {s['tenth_percentage'] or '—'}")
        col4.markdown(f"**12th Year:** {s['twelfth_year'] or '—'}")
        col4.markdown(f"**12th %:** {s['twelfth_percentage'] or '—'}")
        col5.markdown(f"**Grad Year:** {s['grad_year'] or '—'}")
        col5.markdown(f"**Grad GPA:** {s['grad_gpa'] or '—'}")
        get_resume_download_button(s.get('resume_path', ''))

    elif sub == 'add':
        st.subheader("Add New Student")
        if st.button("← Back"):
            st.session_state['faculty_student_sub'] = 'list'
            st.rerun()
        with st.form("faculty_add_student"):
            name     = st.text_input("Full Name *")
            email    = st.text_input("Email *")
            password = st.text_input("Password *", type="password")
            address  = st.text_area("Address")
            gender   = st.selectbox("Gender", ["Male", "Female", "Other"])
            dob      = st.date_input("Date of Birth")
            phone    = st.text_input("Phone")
            branch   = st.text_input("Branch")
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
                st.success("Student added!")
                st.session_state['faculty_student_sub'] = 'list'
                st.rerun()

    elif sub == 'edit':
        sid = st.session_state.get('sel_student_id')
        s   = get_student_by_id(sid) if sid else None
        if not s:
            st.error("Student not found.")
            st.session_state['faculty_student_sub'] = 'list'
            st.rerun()
            return
        if st.button("← Back"):
            st.session_state['faculty_student_sub'] = 'list'
            st.rerun()
        st.subheader(f"Edit Student — {s['name']}")
        with st.form("faculty_edit_student"):
            name    = st.text_input("Full Name",  value=s['name'])
            address = st.text_area("Address",     value=s['address'] or '')
            gender  = st.selectbox("Gender", ["Male","Female","Other"],
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
            st.success("Student updated!")
            st.session_state['faculty_student_sub'] = 'list'
            st.rerun()
