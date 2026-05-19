"""
auth.py — Authentication helpers
Training & Placement Cell Management System
"""

import bcrypt
import re
import streamlit as st
from database import (
    get_user_by_email_and_role, email_exists,
    insert_user, insert_student, insert_faculty, insert_company,
    update_user_password
)


# ─────────────────────────────────────────────
# Password utilities
# ─────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


# ─────────────────────────────────────────────
# Email validation
# ─────────────────────────────────────────────

def is_valid_email(email: str) -> bool:
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email))


# ─────────────────────────────────────────────
# Login
# ─────────────────────────────────────────────

def login(email: str, password: str, role: str) -> tuple[bool, str]:
    """
    Returns (success, message).
    On success sets st.session_state keys.
    """
    if not is_valid_email(email):
        return False, "Invalid email format."

    user = get_user_by_email_and_role(email, role)
    if not user:
        return False, "No user found with this email and role."

    if not verify_password(password, user['password']):
        return False, "Incorrect password."

    st.session_state['logged_in'] = True
    st.session_state['role']      = user['role']
    st.session_state['email']     = user['email']
    st.session_state['name']      = user['name']
    st.session_state['page']      = 'dashboard'
    return True, "Login successful."


# ─────────────────────────────────────────────
# Sign up helpers
# ─────────────────────────────────────────────

def signup_step1(name: str, email: str, password: str,
                 confirm: str, role: str) -> tuple[bool, str]:
    if not is_valid_email(email):
        return False, "Invalid email format."
    if email_exists(email):
        return False, "An account with this email already exists."
    if password != confirm:
        return False, "Passwords do not match."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    st.session_state['signup'] = {
        'name':     name,
        'email':    email,
        'password': password,
        'role':     role,
    }
    return True, "Step 1 complete."


def signup_step2_student(extra: dict) -> tuple[bool, str]:
    data = st.session_state.get('signup', {})
    if not data:
        return False, "Session expired. Please start again."

    pwd_hash = hash_password(data['password'])

    try:
        insert_user(data['name'], data['email'], pwd_hash, 'student')
        insert_student({
            'name':     data['name'],
            'email':    data['email'],
            'password': pwd_hash,
            **extra
        })
        st.session_state.pop('signup', None)
        return True, "Student account created successfully!"
    except Exception as e:
        return False, f"Registration failed: {e}"


def signup_step2_faculty(extra: dict) -> tuple[bool, str]:
    data = st.session_state.get('signup', {})
    if not data:
        return False, "Session expired. Please start again."

    pwd_hash = hash_password(data['password'])

    try:
        insert_user(data['name'], data['email'], pwd_hash, 'faculty')
        insert_faculty({
            'name':     data['name'],
            'email':    data['email'],
            'password': pwd_hash,
            **extra
        })
        st.session_state.pop('signup', None)
        return True, "Faculty account created successfully!"
    except Exception as e:
        return False, f"Registration failed: {e}"


def signup_step2_company(extra: dict) -> tuple[bool, str]:
    data = st.session_state.get('signup', {})
    if not data:
        return False, "Session expired. Please start again."

    pwd_hash = hash_password(data['password'])

    try:
        insert_user(data['name'], data['email'], pwd_hash, 'company')
        insert_company({
            'name':     data['name'],
            'email':    data['email'],
            'password': pwd_hash,
            **extra
        })
        st.session_state.pop('signup', None)
        return True, "Company account created successfully!"
    except Exception as e:
        return False, f"Registration failed: {e}"


# ─────────────────────────────────────────────
# Change password
# ─────────────────────────────────────────────

def change_password(email: str, current: str,
                    new: str, confirm: str) -> tuple[bool, str]:
    from database import get_user_by_email
    user = get_user_by_email(email)
    if not user:
        return False, "User not found."
    if not verify_password(current, user['password']):
        return False, "Current password is incorrect."
    if new != confirm:
        return False, "New passwords do not match."
    if len(new) < 6:
        return False, "New password must be at least 6 characters."

    new_hash = hash_password(new)
    update_user_password(email, new_hash)
    return True, "Password changed successfully!"


# ─────────────────────────────────────────────
# Logout
# ─────────────────────────────────────────────

def logout():
    for key in ['logged_in', 'role', 'email', 'name', 'page', 'signup']:
        st.session_state.pop(key, None)


# ─────────────────────────────────────────────
# Auth guard
# ─────────────────────────────────────────────

def require_login(role: str | None = None):
    """Call at the top of every page. Stops rendering if not authenticated."""
    if not st.session_state.get('logged_in'):
        st.warning("Please log in to access this page.")
        st.stop()
    if role and st.session_state.get('role') != role:
        st.error("Access denied. You don't have permission to view this page.")
        st.stop()
