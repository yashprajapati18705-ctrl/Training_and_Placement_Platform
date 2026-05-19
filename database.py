"""
database.py — All DB connection and query functions
Training & Placement Cell Management System
MySQL implementation
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Connection
# ─────────────────────────────────────────────

def get_connection():
    """Return a new MySQL connection."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "training_db"),
        autocommit=False
    )


# ─────────────────────────────────────────────
# Database initialisation
# ─────────────────────────────────────────────

def init_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        autocommit=True
    )
    cur = conn.cursor()

    # Create database if it doesn't exist
    db_name = os.getenv("DB_NAME", "training_db")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
    cur.execute(f"USE `{db_name}`")

    ddl = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id       INT          PRIMARY KEY AUTO_INCREMENT,
            name     VARCHAR(100) NOT NULL,
            email    VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role     ENUM('admin','student','faculty','company') NOT NULL,
            INDEX idx_email (email),
            INDEX idx_role  (role)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS students (
            id                  INT          PRIMARY KEY AUTO_INCREMENT,
            name                VARCHAR(100) NOT NULL,
            address             TEXT,
            gender              VARCHAR(10),
            dob                 DATE,
            phone               VARCHAR(15),
            branch              VARCHAR(100),
            email               VARCHAR(100) UNIQUE,
            password            VARCHAR(255),
            tenth_year          YEAR,
            tenth_percentage    DECIMAL(5,2),
            twelfth_year        YEAR,
            twelfth_percentage  DECIMAL(5,2),
            grad_year           YEAR,
            grad_gpa            DECIMAL(4,2),
            resume_path         VARCHAR(255),
            INDEX idx_email (email)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS faculties (
            id         INT          PRIMARY KEY AUTO_INCREMENT,
            name       VARCHAR(100) NOT NULL,
            address    TEXT,
            gender     VARCHAR(10),
            department VARCHAR(100),
            phone      VARCHAR(15),
            email      VARCHAR(100) UNIQUE,
            password   VARCHAR(255),
            INDEX idx_email (email)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS companies (
            id       INT          PRIMARY KEY AUTO_INCREMENT,
            name     VARCHAR(100) NOT NULL UNIQUE,
            address  TEXT,
            website  VARCHAR(255),
            phone    VARCHAR(15),
            email    VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            INDEX idx_email (email)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id                 INT          PRIMARY KEY AUTO_INCREMENT,
            name               VARCHAR(100) NOT NULL,
            designation        VARCHAR(100) NOT NULL,
            description        TEXT,
            experience         VARCHAR(100),
            twelfth_percentage DECIMAL(5,2),
            grad_gpa           DECIMAL(4,2),
            seats              INT,
            salary_package     VARCHAR(50),
            INDEX idx_company (name)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS applied_jobs (
            id            INT          PRIMARY KEY AUTO_INCREMENT,
            company_name  VARCHAR(100) NOT NULL,
            student_name  VARCHAR(100) NOT NULL,
            student_email VARCHAR(100) NOT NULL,
            designation   VARCHAR(100),
            apply_date    DATETIME     DEFAULT NOW(),
            status        VARCHAR(50)  DEFAULT 'Applied',
            INDEX idx_student_email (student_email),
            INDEX idx_company       (company_name)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS selected_students (
            id            INT          PRIMARY KEY AUTO_INCREMENT,
            student_name  VARCHAR(100) NOT NULL,
            student_email VARCHAR(100),
            branch        VARCHAR(100),
            company_name  VARCHAR(100) NOT NULL,
            role          VARCHAR(100),
            salary        VARCHAR(50),
            INDEX idx_company (company_name)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS college_info (
            id      INT          PRIMARY KEY AUTO_INCREMENT,
            field   VARCHAR(100) NOT NULL UNIQUE,
            value   TEXT
        )
        """
    ]

    for stmt in ddl:
        cur.execute(stmt)

    # Seed college info
    cur.execute("SELECT COUNT(*) FROM college_info")
    if cur.fetchone()[0] == 0:
        rows = [
            ("College Name",    "ABC Engineering College"),
            ("Address",         "123 College Road, City - 000000"),
            ("Contact",         "+91-9999999999"),
            ("Email",           "principal@abcengg.edu"),
            ("Website",         "https://www.abcengg.edu"),
            ("Established",     "1990"),
        ]
        cur.executemany(
            "INSERT INTO college_info (field, value) VALUES (%s, %s)",
            rows
        )

    # Seed admin account
    cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if cur.fetchone()[0] == 0:
        import bcrypt
        hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        cur.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'admin')",
            ("Admin", "admin@tp.com", hashed)
        )

    cur.close()
    conn.close()


# ─────────────────────────────────────────────
# Generic helpers
# ─────────────────────────────────────────────

def execute_query(sql, params=None, fetch=None):
    """
    Execute a SQL statement.
    fetch: None (commit), 'one', 'all'
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, params or ())
        if fetch == 'one':
            result = cur.fetchone()
        elif fetch == 'all':
            result = cur.fetchall()
        else:
            conn.commit()
            result = cur.lastrowid
        return result
    except Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# Users
# ─────────────────────────────────────────────

def get_user_by_email(email):
    return execute_query("SELECT * FROM users WHERE email=%s", (email,), fetch='one')

def get_user_by_email_and_role(email, role):
    return execute_query(
        "SELECT * FROM users WHERE email=%s AND role=%s", (email, role), fetch='one'
    )

def email_exists(email):
    row = execute_query("SELECT id FROM users WHERE email=%s", (email,), fetch='one')
    return row is not None

def insert_user(name, email, password_hash, role):
    execute_query(
        "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
        (name, email, password_hash, role)
    )

def update_user_password(email, new_hash):
    execute_query(
        "UPDATE users SET password=%s WHERE email=%s", (new_hash, email)
    )

def delete_user_by_email(email):
    execute_query("DELETE FROM users WHERE email=%s", (email,))


# ─────────────────────────────────────────────
# Students
# ─────────────────────────────────────────────

def get_all_students():
    return execute_query("SELECT * FROM students ORDER BY id", fetch='all')

def get_student_by_email(email):
    return execute_query("SELECT * FROM students WHERE email=%s", (email,), fetch='one')

def get_student_by_id(sid):
    return execute_query("SELECT * FROM students WHERE id=%s", (sid,), fetch='one')

def insert_student(data: dict):
    sql = """
        INSERT INTO students
            (name, address, gender, dob, phone, branch, email, password)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    execute_query(sql, (
        data['name'], data['address'], data['gender'], data['dob'],
        data['phone'], data['branch'], data['email'], data['password']
    ))

def update_student(sid, data: dict):
    sql = """
        UPDATE students SET
            name=%s, address=%s, gender=%s, dob=%s,
            phone=%s, branch=%s
        WHERE id=%s
    """
    execute_query(sql, (
        data['name'], data['address'], data['gender'], data['dob'],
        data['phone'], data['branch'], sid
    ))

def update_student_academic(email, data: dict):
    sql = """
        UPDATE students SET
            tenth_year=%s, tenth_percentage=%s,
            twelfth_year=%s, twelfth_percentage=%s,
            grad_year=%s, grad_gpa=%s, resume_path=%s
        WHERE email=%s
    """
    execute_query(sql, (
        data['tenth_year'], data['tenth_percentage'],
        data['twelfth_year'], data['twelfth_percentage'],
        data['grad_year'], data['grad_gpa'],
        data['resume_path'], email
    ))

def delete_student(sid):
    student = get_student_by_id(sid)
    if student:
        execute_query("DELETE FROM students WHERE id=%s", (sid,))
        delete_user_by_email(student['email'])


# ─────────────────────────────────────────────
# Faculties
# ─────────────────────────────────────────────

def get_all_faculties():
    return execute_query("SELECT * FROM faculties ORDER BY id", fetch='all')

def get_faculty_by_email(email):
    return execute_query("SELECT * FROM faculties WHERE email=%s", (email,), fetch='one')

def get_faculty_by_id(fid):
    return execute_query("SELECT * FROM faculties WHERE id=%s", (fid,), fetch='one')

def insert_faculty(data: dict):
    sql = """
        INSERT INTO faculties
            (name, address, gender, department, phone, email, password)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    execute_query(sql, (
        data['name'], data['address'], data['gender'], data['department'],
        data['phone'], data['email'], data['password']
    ))

def update_faculty(fid, data: dict):
    sql = """
        UPDATE faculties SET
            name=%s, address=%s, gender=%s, department=%s, phone=%s
        WHERE id=%s
    """
    execute_query(sql, (
        data['name'], data['address'], data['gender'],
        data['department'], data['phone'], fid
    ))

def delete_faculty(fid):
    faculty = get_faculty_by_id(fid)
    if faculty:
        execute_query("DELETE FROM faculties WHERE id=%s", (fid,))
        delete_user_by_email(faculty['email'])


# ─────────────────────────────────────────────
# Companies
# ─────────────────────────────────────────────

def get_all_companies():
    return execute_query("SELECT * FROM companies ORDER BY id", fetch='all')

def get_company_by_email(email):
    return execute_query("SELECT * FROM companies WHERE email=%s", (email,), fetch='one')

def get_company_by_id(cid):
    return execute_query("SELECT * FROM companies WHERE id=%s", (cid,), fetch='one')

def insert_company(data: dict):
    sql = """
        INSERT INTO companies
            (name, address, website, phone, email, password)
        VALUES (%s,%s,%s,%s,%s,%s)
    """
    execute_query(sql, (
        data['name'], data['address'], data['website'],
        data['phone'], data['email'], data['password']
    ))

def update_company(cid, data: dict):
    sql = """
        UPDATE companies SET
            name=%s, address=%s, website=%s, phone=%s
        WHERE id=%s
    """
    execute_query(sql, (
        data['name'], data['address'], data['website'], data['phone'], cid
    ))

def delete_company(cid):
    company = get_company_by_id(cid)
    if company:
        execute_query("DELETE FROM companies WHERE id=%s", (cid,))
        delete_user_by_email(company['email'])


# ─────────────────────────────────────────────
# Jobs
# ─────────────────────────────────────────────

def get_all_jobs():
    return execute_query("SELECT * FROM jobs ORDER BY id", fetch='all')

def get_jobs_by_company(company_name):
    return execute_query(
        "SELECT * FROM jobs WHERE name=%s ORDER BY id", (company_name,), fetch='all'
    )

def get_job_by_id(jid):
    return execute_query("SELECT * FROM jobs WHERE id=%s", (jid,), fetch='one')

def insert_job(data: dict):
    sql = """
        INSERT INTO jobs
            (name, designation, description, experience,
             twelfth_percentage, grad_gpa, seats, salary_package)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    execute_query(sql, (
        data['name'], data['designation'], data['description'],
        data['experience'], data['twelfth_percentage'], data['grad_gpa'],
        data['seats'], data['salary_package']
    ))

def delete_job(jid):
    execute_query("DELETE FROM jobs WHERE id=%s", (jid,))

def decrement_job_seats(company_name, designation):
    execute_query(
        "UPDATE jobs SET seats = seats - 1 WHERE name=%s AND designation=%s",
        (company_name, designation)
    )
    job = execute_query(
        "SELECT id, seats FROM jobs WHERE name=%s AND designation=%s",
        (company_name, designation), fetch='one'
    )
    if job and job['seats'] is not None and job['seats'] <= 0:
        delete_job(job['id'])


# ─────────────────────────────────────────────
# Applied Jobs
# ─────────────────────────────────────────────

def get_applied_jobs_by_student(student_email):
    return execute_query(
        "SELECT * FROM applied_jobs WHERE student_email=%s ORDER BY apply_date DESC",
        (student_email,), fetch='all'
    )

def get_applied_jobs_by_company(company_name):
    return execute_query(
        "SELECT * FROM applied_jobs WHERE company_name=%s ORDER BY apply_date DESC",
        (company_name,), fetch='all'
    )

def get_application_by_id(aid):
    return execute_query(
        "SELECT * FROM applied_jobs WHERE id=%s", (aid,), fetch='one'
    )

def student_already_applied(student_email):
    row = execute_query(
        "SELECT id FROM applied_jobs WHERE student_email=%s", (student_email,), fetch='one'
    )
    return row is not None

def insert_application(data: dict):
    sql = """
        INSERT INTO applied_jobs
            (company_name, student_name, student_email, designation)
        VALUES (%s,%s,%s,%s)
    """
    execute_query(sql, (
        data['company_name'], data['student_name'],
        data['student_email'], data['designation']
    ))

def reject_application(aid):
    execute_query(
        "UPDATE applied_jobs SET status='Rejected' WHERE id=%s", (aid,)
    )

def approve_application(aid):
    """
    Move student from applied_jobs → selected_students.
    Decrement seats; auto-delete job if seats = 0.
    """
    app = get_application_by_id(aid)
    if not app:
        return False

    student = get_student_by_email(app['student_email'])
    job = execute_query(
        "SELECT * FROM jobs WHERE name=%s AND designation=%s",
        (app['company_name'], app['designation']), fetch='one'
    )

    branch = student['branch'] if student else 'N/A'
    salary = job['salary_package'] if job else 'N/A'
    role   = app['designation']

    # Insert into selected_students
    execute_query(
        """
        INSERT INTO selected_students
            (student_name, student_email, branch, company_name, role, salary)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (app['student_name'], app['student_email'], branch,
         app['company_name'], role, salary)
    )

    # Remove application
    execute_query("DELETE FROM applied_jobs WHERE id=%s", (aid,))

    # Decrement seats / remove job if 0
    decrement_job_seats(app['company_name'], app['designation'])
    return True


# ─────────────────────────────────────────────
# Selected Students
# ─────────────────────────────────────────────

def get_all_selected_students():
    return execute_query("SELECT * FROM selected_students ORDER BY id", fetch='all')


# ─────────────────────────────────────────────
# College Info
# ─────────────────────────────────────────────

def get_college_info():
    rows = execute_query("SELECT field, value FROM college_info", fetch='all')
    return {r['field']: r['value'] for r in rows} if rows else {}

def update_college_info(info: dict):
    for field, value in info.items():
        execute_query(
            "INSERT INTO college_info (field, value) VALUES (%s,%s) "
            "ON DUPLICATE KEY UPDATE value=%s",
            (field, value, value)
        )


# ─────────────────────────────────────────────
# Dashboard Counts
# ─────────────────────────────────────────────

def get_dashboard_counts():
    def count(table):
        row = execute_query(f"SELECT COUNT(*) AS cnt FROM {table}", fetch='one')
        return row['cnt'] if row else 0

    return {
        'students':          count('students'),
        'faculties':         count('faculties'),
        'companies':         count('companies'),
        'selected_students': count('selected_students'),
    }
