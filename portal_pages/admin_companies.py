"""Admin — Company Management (CRUD)."""

import streamlit as st
from auth import require_login, hash_password
from database import (
    get_all_companies, get_company_by_id,
    insert_company, insert_user, update_company, delete_company, email_exists
)


def render():
    require_login('admin')
    st.title("🏢 Companies Management")

    sub = st.session_state.get('admin_company_sub', 'list')

    # ── List ──────────────────────────────────
    if sub == 'list':
        st.subheader("All Companies")
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("➕ Add New Company", use_container_width=True):
                st.session_state['admin_company_sub'] = 'add'
                st.rerun()

        companies = get_all_companies()
        if not companies:
            st.info("No companies registered yet.")
            return

        for c in companies:
            with st.expander(f"#{c['id']}  {c['name']}  |  {c['email']}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("👁 View",   key=f"vc_{c['id']}", use_container_width=True):
                        st.session_state['admin_company_sub'] = 'view'
                        st.session_state['sel_company_id']    = c['id']
                        st.rerun()
                with c2:
                    if st.button("✏️ Edit",  key=f"ec_{c['id']}", use_container_width=True):
                        st.session_state['admin_company_sub'] = 'edit'
                        st.session_state['sel_company_id']    = c['id']
                        st.rerun()
                with c3:
                    if st.button("🗑 Delete", key=f"dc_{c['id']}", use_container_width=True):
                        delete_company(c['id'])
                        st.success(f"Company '{c['name']}' deleted.")
                        st.rerun()

    # ── Add ───────────────────────────────────
    elif sub == 'add':
        st.subheader("Add New Company")
        if st.button("← Back to List"):
            st.session_state['admin_company_sub'] = 'list'
            st.rerun()

        with st.form("add_company_form"):
            name      = st.text_input("Company Name *")
            email     = st.text_input("Email *")
            password  = st.text_input("Password *", type="password")
            address   = st.text_area("Address")
            website   = st.text_input("Website URL")
            phone     = st.text_input("Phone")
            submitted = st.form_submit_button("Add Company")

        if submitted:
            if not name or not email or not password:
                st.error("Company Name, Email, and Password are required.")
            elif email_exists(email):
                st.error("Email already registered.")
            else:
                pwd_hash = hash_password(password)
                insert_user(name, email, pwd_hash, 'company')
                insert_company({
                    'name': name, 'address': address, 'website': website,
                    'phone': phone, 'email': email, 'password': pwd_hash
                })
                st.success(f"Company '{name}' added successfully!")
                st.session_state['admin_company_sub'] = 'list'
                st.rerun()

    # ── View ──────────────────────────────────
    elif sub == 'view':
        cid = st.session_state.get('sel_company_id')
        c   = get_company_by_id(cid) if cid else None
        if not c:
            st.error("Company not found.")
            st.session_state['admin_company_sub'] = 'list'
            st.rerun()
            return

        if st.button("← Back to List"):
            st.session_state['admin_company_sub'] = 'list'
            st.rerun()

        st.subheader(f"Company Profile — {c['name']}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** {c['name']}")
            st.markdown(f"**Email:** {c['email']}")
            st.markdown(f"**Phone:** {c['phone'] or '—'}")
        with col2:
            st.markdown(f"**Website:** {c['website'] or '—'}")
            st.markdown(f"**Address:** {c['address'] or '—'}")

    # ── Edit ──────────────────────────────────
    elif sub == 'edit':
        cid = st.session_state.get('sel_company_id')
        c   = get_company_by_id(cid) if cid else None
        if not c:
            st.error("Company not found.")
            st.session_state['admin_company_sub'] = 'list'
            st.rerun()
            return

        if st.button("← Back to List"):
            st.session_state['admin_company_sub'] = 'list'
            st.rerun()

        st.subheader(f"Edit Company — {c['name']}")
        with st.form("edit_company_form"):
            name      = st.text_input("Company Name", value=c['name'])
            address   = st.text_area("Address",       value=c['address'] or '')
            website   = st.text_input("Website",      value=c['website'] or '')
            phone     = st.text_input("Phone",        value=c['phone'] or '')
            submitted = st.form_submit_button("Update Company")

        if submitted:
            update_company(cid, {
                'name': name, 'address': address,
                'website': website, 'phone': phone
            })
            st.success("Company updated successfully!")
            st.session_state['admin_company_sub'] = 'list'
            st.rerun()
