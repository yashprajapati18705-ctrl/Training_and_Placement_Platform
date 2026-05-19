"""Admin — Faculty Management (CRUD)."""

import streamlit as st
from auth import require_login, hash_password
from database import (
    get_all_faculties, get_faculty_by_id,
    insert_faculty, insert_user, update_faculty, delete_faculty, email_exists
)


def render():
    require_login('admin')
    st.title("👨‍🏫 Faculty Management")

    sub = st.session_state.get('admin_faculty_sub', 'list')

    # ── List ──────────────────────────────────
    if sub == 'list':
        st.subheader("All Faculty Members")
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("➕ Add New Faculty", use_container_width=True):
                st.session_state['admin_faculty_sub'] = 'add'
                st.rerun()

        faculties = get_all_faculties()
        if not faculties:
            st.info("No faculty members registered yet.")
            return

        for f in faculties:
            with st.expander(f"#{f['id']}  {f['name']}  |  {f['department'] or '—'}  |  {f['email']}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("👁 View",   key=f"vf_{f['id']}", use_container_width=True):
                        st.session_state['admin_faculty_sub'] = 'view'
                        st.session_state['sel_faculty_id']    = f['id']
                        st.rerun()
                with c2:
                    if st.button("✏️ Edit",  key=f"ef_{f['id']}", use_container_width=True):
                        st.session_state['admin_faculty_sub'] = 'edit'
                        st.session_state['sel_faculty_id']    = f['id']
                        st.rerun()
                with c3:
                    if st.button("🗑 Delete", key=f"df_{f['id']}", use_container_width=True):
                        delete_faculty(f['id'])
                        st.success(f"Faculty '{f['name']}' deleted.")
                        st.rerun()

    # ── Add ───────────────────────────────────
    elif sub == 'add':
        st.subheader("Add New Faculty Member")
        if st.button("← Back to List"):
            st.session_state['admin_faculty_sub'] = 'list'
            st.rerun()

        with st.form("add_faculty_form"):
            name       = st.text_input("Full Name *")
            email      = st.text_input("Email *")
            password   = st.text_input("Password *", type="password")
            address    = st.text_area("Address")
            gender     = st.selectbox("Gender", ["Male", "Female", "Other"])
            department = st.text_input("Department")
            phone      = st.text_input("Phone")
            submitted  = st.form_submit_button("Add Faculty")

        if submitted:
            if not name or not email or not password:
                st.error("Name, Email, and Password are required.")
            elif email_exists(email):
                st.error("Email already registered.")
            else:
                pwd_hash = hash_password(password)
                insert_user(name, email, pwd_hash, 'faculty')
                insert_faculty({
                    'name': name, 'address': address, 'gender': gender.lower(),
                    'department': department, 'phone': phone,
                    'email': email, 'password': pwd_hash
                })
                st.success(f"Faculty '{name}' added successfully!")
                st.session_state['admin_faculty_sub'] = 'list'
                st.rerun()

    # ── View ──────────────────────────────────
    elif sub == 'view':
        fid = st.session_state.get('sel_faculty_id')
        f   = get_faculty_by_id(fid) if fid else None
        if not f:
            st.error("Faculty not found.")
            st.session_state['admin_faculty_sub'] = 'list'
            st.rerun()
            return

        if st.button("← Back to List"):
            st.session_state['admin_faculty_sub'] = 'list'
            st.rerun()

        st.subheader(f"Faculty Profile — {f['name']}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** {f['name']}")
            st.markdown(f"**Email:** {f['email']}")
            st.markdown(f"**Phone:** {f['phone'] or '—'}")
            st.markdown(f"**Gender:** {f['gender'] or '—'}")
        with col2:
            st.markdown(f"**Department:** {f['department'] or '—'}")
            st.markdown(f"**Address:** {f['address'] or '—'}")

    # ── Edit ──────────────────────────────────
    elif sub == 'edit':
        fid = st.session_state.get('sel_faculty_id')
        f   = get_faculty_by_id(fid) if fid else None
        if not f:
            st.error("Faculty not found.")
            st.session_state['admin_faculty_sub'] = 'list'
            st.rerun()
            return

        if st.button("← Back to List"):
            st.session_state['admin_faculty_sub'] = 'list'
            st.rerun()

        st.subheader(f"Edit Faculty — {f['name']}")
        with st.form("edit_faculty_form"):
            name       = st.text_input("Full Name",   value=f['name'])
            address    = st.text_area("Address",      value=f['address'] or '')
            gender     = st.selectbox("Gender", ["Male", "Female", "Other"],
                                      index=["male", "female", "other"].index(
                                          (f['gender'] or 'male').lower()))
            department = st.text_input("Department",  value=f['department'] or '')
            phone      = st.text_input("Phone",       value=f['phone'] or '')
            submitted  = st.form_submit_button("Update Faculty")

        if submitted:
            update_faculty(fid, {
                'name': name, 'address': address, 'gender': gender.lower(),
                'department': department, 'phone': phone
            })
            st.success("Faculty updated successfully!")
            st.session_state['admin_faculty_sub'] = 'list'
            st.rerun()
