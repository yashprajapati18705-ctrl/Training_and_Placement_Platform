"""Company — Home (Profile)."""

import streamlit as st
from auth import require_login
from database import get_company_by_email


def render():
    require_login('company')
    st.title("🏢 Company Profile")
    st.markdown("---")

    email   = st.session_state.get('email')
    company = get_company_by_email(email)

    if not company:
        st.error("Profile data not found. Please contact the administrator.")
        return

    st.markdown(f"**Company Name:** {company['name']}")
    st.markdown(f"**Email:** {company['email']}")
    st.markdown(f"**Phone:** {company['phone'] or '—'}")
    st.markdown(f"**Website:** {company['website'] or '—'}")
    st.markdown(f"**Address:** {company['address'] or '—'}")
