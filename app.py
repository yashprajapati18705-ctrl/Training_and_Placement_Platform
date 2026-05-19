
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from database import init_db
from auth import login, signup_step1, signup_step2_student, signup_step2_faculty, signup_step2_company, is_valid_email
from database import get_user_by_email, update_user_password
from auth import hash_password

st.set_page_config(
    page_title="T&P Cell Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

HIDE_SIDEBAR_CSS = """
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
</style>
"""

@st.cache_resource
def bootstrap():
    init_db()
    return True

bootstrap()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'auth_page' not in st.session_state:
    st.session_state['auth_page'] = 'login'


def import_page(module_name: str):
    import importlib
    mod = importlib.import_module(f"portal_pages.{module_name}")
    return mod


# ── AUTHENTICATED ─────────────────────────────
if st.session_state.get('logged_in'):
    role = st.session_state.get('role')
    name = st.session_state.get('name', '')

    with st.sidebar:
        st.markdown(f"### 👤 {name}")
        st.markdown(f"*Role: {role.capitalize()}*")
        st.markdown("---")

    if role == 'admin':
        with st.sidebar:
            pages = {
                "🏠 Dashboard":         "dashboard",
                "🎓 Students":          "students",
                "👨‍🏫 Faculty":          "faculty",
                "🏢 Companies":         "companies",
                "💼 Openings":          "openings",
                "✅ Selected Students": "selected",
                "🏛️ College Info":      "college_info",
                "🔑 Change Password":   "change_password",
            }
            for label, key in pages.items():
                if st.button(label, use_container_width=True, key=f"admin_nav_{key}"):
                    st.session_state['page'] = key
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                from auth import logout
                logout()
                st.rerun()

        page = st.session_state.get('page', 'dashboard')
        if page == 'dashboard':       import_page('admin_dashboard').render()
        elif page == 'students':      import_page('admin_students').render()
        elif page == 'faculty':       import_page('admin_faculty').render()
        elif page == 'companies':     import_page('admin_companies').render()
        elif page == 'openings':      import_page('admin_openings').render()
        elif page == 'selected':      import_page('admin_selected').render()
        elif page == 'college_info':  import_page('admin_college_info').render()
        elif page == 'change_password': import_page('change_password').render()

    elif role == 'student':
        with st.sidebar:
            pages = {
                "🏠 Home":            "home",
                "📤 Upload Info":     "upload",
                "💼 Openings":        "openings",
                "📋 Applied Jobs":    "applied",
                "🔑 Change Password": "change_password",
            }
            for label, key in pages.items():
                if st.button(label, use_container_width=True, key=f"student_nav_{key}"):
                    st.session_state['page'] = key
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                from auth import logout
                logout()
                st.rerun()

        page = st.session_state.get('page', 'home')
        if page == 'home':            import_page('student_home').render()
        elif page == 'upload':        import_page('student_upload').render()
        elif page == 'openings':      import_page('student_openings').render()
        elif page == 'applied':       import_page('student_applied').render()
        elif page == 'change_password': import_page('change_password').render()

    elif role == 'faculty':
        with st.sidebar:
            pages = {
                "🏠 Home":              "home",
                "🎓 Students":          "students",
                "🚀 Placement Drive":   "drives",
                "✅ Selected Students": "selected",
                "🔑 Change Password":   "change_password",
            }
            for label, key in pages.items():
                if st.button(label, use_container_width=True, key=f"faculty_nav_{key}"):
                    st.session_state['page'] = key
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                from auth import logout
                logout()
                st.rerun()

        page = st.session_state.get('page', 'home')
        if page == 'home':            import_page('faculty_home').render()
        elif page == 'students':      import_page('faculty_students').render()
        elif page == 'drives':        import_page('faculty_drives').render()
        elif page == 'selected':      import_page('faculty_selected').render()
        elif page == 'change_password': import_page('change_password').render()

    elif role == 'company':
        with st.sidebar:
            pages = {
                "🏠 Home":            "home",
                "💼 Jobs":            "jobs",
                "📋 Applications":    "applications",
                "🔑 Change Password": "change_password",
            }
            for label, key in pages.items():
                if st.button(label, use_container_width=True, key=f"company_nav_{key}"):
                    st.session_state['page'] = key
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                from auth import logout
                logout()
                st.rerun()

        page = st.session_state.get('page', 'home')
        if page == 'home':            import_page('company_home').render()
        elif page == 'jobs':          import_page('company_jobs').render()
        elif page == 'applications':  import_page('company_applications').render()
        elif page == 'change_password': import_page('change_password').render()

# ── UNAUTHENTICATED ───────────────────────────
else:
    st.markdown(HIDE_SIDEBAR_CSS, unsafe_allow_html=True)
    auth_page = st.session_state.get('auth_page', 'login')

    if auth_page == 'login':
        st.title("🎓 Training & Placement Cell")
        st.subheader("Login")
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                role     = st.selectbox("Login As", ["Admin", "Student", "Faculty", "Company"])
                email    = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("🔐 Login", use_container_width=True)
            if submitted:
                ok, msg = login(email, password, role.lower())
                if ok:
                    st.rerun()
                else:
                    st.error(msg)
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("📝 Sign Up", use_container_width=True):
                    st.session_state['auth_page'] = 'signup1'
                    st.rerun()
            with c2:
                if st.button("🔓 Forgot Password", use_container_width=True):
                    st.session_state['auth_page'] = 'forgot'
                    st.rerun()

    elif auth_page == 'signup1':
        st.title("📝 Create Account — Step 1")
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("signup1_form"):
                role     = st.selectbox("Register As", ["Student", "Faculty", "Company"])
                name     = st.text_input("Full Name *")
                email    = st.text_input("Email *")
                password = st.text_input("Password *", type="password")
                confirm  = st.text_input("Confirm Password *", type="password")
                submitted = st.form_submit_button("Next ➡️", use_container_width=True)
            if submitted:
                ok, msg = signup_step1(name, email, password, confirm, role.lower())
                if ok:
                    st.session_state['auth_page'] = 'signup2'
                    st.rerun()
                else:
                    st.error(msg)
            if st.button("← Back to Login"):
                st.session_state['auth_page'] = 'login'
                st.rerun()

    elif auth_page == 'signup2':
        data = st.session_state.get('signup', {})
        role = data.get('role', 'student')
        st.title(f"📝 Complete Registration — {role.capitalize()}")
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if role == 'student':
                with st.form("signup2_student"):
                    address = st.text_area("Address")
                    phone   = st.text_input("Phone")
                    dob     = st.date_input("Date of Birth")
                    gender  = st.selectbox("Gender", ["Male", "Female", "Other"])
                    branch  = st.text_input("Branch (e.g., Computer Engineering)")
                    submitted = st.form_submit_button("✅ Register", use_container_width=True)
                if submitted:
                    ok, msg = signup_step2_student({
                        'address': address, 'phone': phone, 'dob': dob,
                        'gender': gender.lower(), 'branch': branch
                    })
                    if ok:
                        st.success(msg + " Please login.")
                        st.session_state['auth_page'] = 'login'
                        st.rerun()
                    else:
                        st.error(msg)

            elif role == 'faculty':
                with st.form("signup2_faculty"):
                    address    = st.text_area("Address")
                    phone      = st.text_input("Phone")
                    department = st.text_input("Department")
                    gender     = st.selectbox("Gender", ["Male", "Female", "Other"])
                    submitted  = st.form_submit_button("✅ Register", use_container_width=True)
                if submitted:
                    ok, msg = signup_step2_faculty({
                        'address': address, 'phone': phone,
                        'department': department, 'gender': gender.lower()
                    })
                    if ok:
                        st.success(msg + " Please login.")
                        st.session_state['auth_page'] = 'login'
                        st.rerun()
                    else:
                        st.error(msg)

            elif role == 'company':
                with st.form("signup2_company"):
                    address   = st.text_area("Address")
                    phone     = st.text_input("Phone")
                    website   = st.text_input("Website URL")
                    submitted = st.form_submit_button("✅ Register", use_container_width=True)
                if submitted:
                    ok, msg = signup_step2_company({
                        'address': address, 'phone': phone, 'website': website
                    })
                    if ok:
                        st.success(msg + " Please login.")
                        st.session_state['auth_page'] = 'login'
                        st.rerun()
                    else:
                        st.error(msg)

            if st.button("← Back"):
                st.session_state['auth_page'] = 'signup1'
                st.rerun()

    elif auth_page == 'forgot':
        st.title("🔓 Reset Password")
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("forgot_form"):
                email   = st.text_input("Enter your registered Email *")
                new_pwd = st.text_input("New Password *", type="password")
                confirm = st.text_input("Confirm New Password *", type="password")
                submitted = st.form_submit_button("Reset Password", use_container_width=True)
            if submitted:
                if not is_valid_email(email):
                    st.error("Invalid email format.")
                elif new_pwd != confirm:
                    st.error("Passwords do not match.")
                elif len(new_pwd) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    user = get_user_by_email(email)
                    if not user:
                        st.error("No account found with this email.")
                    else:
                        update_user_password(email, hash_password(new_pwd))
                        st.success("Password reset successfully! Please login.")
                        st.session_state['auth_page'] = 'login'
                        st.rerun()
            if st.button("← Back to Login"):
                st.session_state['auth_page'] = 'login'
                st.rerun()
