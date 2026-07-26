# Training and Placement Platform

A web-based Training and Placement Management System developed using Python, Streamlit, and MySQL to streamline placement activities for colleges. The platform enables management of student profiles, company details, job postings, applications, and placement records through an interactive and user-friendly dashboard.

## Project Subtitle

Streamlit-Based College Placement Management System

## Features

- Student registration and profile management
- Company and recruiter management
- Job posting and eligibility criteria management
- Student job application tracking
- Placement status monitoring
- Secure authentication and login system
- Resume and document upload support
- Interactive dashboard and analytics
- Search and filtering functionality

## Technologies Used

### Programming Language
- Python

### Web Framework
- Streamlit

### Database
- MySQL

### Libraries and Tools
- Pandas
- Plotly
- python-dotenv
- mysql-connector-python
- Pillow
- streamlit-option-menu

### Development Tools
- PyCharm
- Git
- GitHub

## Project Structure

```text
Training_and_Placement_Platform/
│── portal_pages/
│── uploads/
│── .env
│── requirements.txt
│── app.py
│── auth.py
│── database.py
│── utils.py
````

## Modules

* **app.py** – Main entry point of the application
* **auth.py** – Handles user authentication and session management
* **database.py** – Database connection and CRUD operations
* **utils.py** – Utility and helper functions
* **portal_pages/** – Contains pages for students, companies, jobs, and analytics
* **uploads/** – Stores uploaded resumes and documents

## Key Functionalities

* Secure login and registration
* Student and recruiter dashboards
* Company and job management
* Application tracking
* Placement analytics and reporting
* Resume upload and storage
* Dynamic charts and data visualization

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yashprajapati18705-ctrl/Training_and_Placement_Platform.git
cd Training_and_Placement_Platform
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / Mac**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=XXXXXXXX
DB_NAME=training_db
```

### 5. Run the Application

```bash
streamlit run app.py
```

## Academic Project

This project was developed as an academic project to automate and digitize the college training and placement process, improving efficiency in managing students, recruiters, job opportunities, and placement outcomes.

## Future Enhancements

* Email notifications to students
* Resume screening using Machine Learning
* Interview scheduling system
* Role-based access control
* Placement prediction analytics

## Author

**Yash Prajapati**
Computer Engineering Student | Data Science & Machine Learning Enthusiast

* LinkedIn: [https://www.linkedin.com/in/yash-prajapati-cse2026/](https://www.linkedin.com/in/yash-prajapati-cse2026/)
* GitHub: [https://github.com/yashprajapati18705-ctrl](https://github.com/yashprajapati18705-ctrl)

## License

This project is developed for educational and academic purposes.