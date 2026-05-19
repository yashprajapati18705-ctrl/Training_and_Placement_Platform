"""Shared — Change Password page (all roles)."""

import streamlit as st
from auth import require_login, change_password


def render():
    if not st.session_state.get('logged_in'):
        st.warning("Please log in first.")
        st.stop()

    st.title("🔑 Change Password")
    st.markdown("---")

    with st.form("change_password_form"):
        current = st.text_input("Current Password",     type="password")
        new     = st.text_input("New Password",         type="password")
        confirm = st.text_input("Confirm New Password", type="password")
        submitted = st.form_submit_button("Update Password")

    if submitted:
        ok, msg = change_password(
            st.session_state.get('email'), current, new, confirm
        )
        if ok:
            st.success(msg)
        else:
            st.error(msg)
