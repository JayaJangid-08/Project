# Task Management API

A Django REST Framework based API to manage projects, tasks, and comments with role-based access control.

There are two apps in TaskManagement API :-  

- **i) Authenticate** :-
  In this App, I've added signup , login and token refresh URLs.
      
- **ii) Tasks** :- 
  In this App, I've added project and tasks detail URLs.  


---

##  Features

-  Authentication (Signup, Login, Token)
-  Role-based access (Admin, Manager, Member)
-  Project Management
-  Task Assignment (single/multiple users)
-  Comment System
-  Due Date Tracking
-  Task Status & Priority
-  Pagination , Filtering.
-  Searching & Sorting.

---

##  Roles & Permissions

###  Admin
- Full access to all projects, tasks, and comments

###  Manager
- Can create projects
- Can assign tasks
- Access only their created/assigned projects

###  Member
- Can view assigned tasks
- Can update their tasks
- Can add/delete comments

---

##  Apps Included

### 1. Authenticate
- Signup
- Login
- Token authentication

### 2. Tasks
- Project APIs
- Task APIs
- Comment APIs

---

## 🔗 API Endpoints

###  Authentication
- `POST /signup/`
- `POST /login/`

---

###  Projects
- `GET /projects/`
- `POST /projects/`
- `GET /projects/{project_id}/`

---

###  Members
- `POST /projects/{project_id}/members/add/`
- `POST /projects/{project_id}/members/remove/`

---

###  Tasks
- `GET /projects/{project_id}/tasks/`
- `POST /projects/{project_id}/tasks/`
- `GET /projects/{project_id}/tasks/{task_id}/`

---

###  Comments
- `GET /projects/{project_id}/tasks/{task_id}/comments/`
- `POST /projects/{project_id}/tasks/{task_id}/comments/`

---

##  Tech Stack

- Python
- Django
- Django REST Framework
- SQLite (default)

---

##  Setup Instructions

```bash
# Clone the repo 'https://github.com/JayaJangid-08/Project.git'
git clone 

# Navigate to project
cd Project

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  (Windows)

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
