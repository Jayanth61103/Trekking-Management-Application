Trekking Management Application

# Install Required Packages for Backend
Step:1 Need to create a Virtual Environment (venv)
Step:2 Activate Virtual Environment (venv)
step:3 Install Packages (flask, flask_restful, flask_sqlalchemy,  )
step:4 Add Packages Required to requirements.txt


'''bash 
python -m venv venv 

.\venv\Scripts\activate # Windows 
source .\venv\bin\activate # Linux & Mac 

pip install flask flask_restful flask_sqlalchemy  flask_jwt_extended # Packages

pip install -r backend_requirements.txt # to download packages from backend requirements.

pip freeze > backend_requirements.txt # Update the package requirements for backend 
'''

# Install Required Packages for Frontend (vue.js)

'''bash
npm install  # To download packages for frontend 
'''# Trekking Management System (TMS)

A full-stack web application developed as part of the IIT Madras Modern Application Development II (MAD 2) course.

## Tech Stack

### Backend
- Python
- Flask
- Flask RESTful
- Flask SQLAlchemy
- Flask JWT Extended
- Flask CORS
- SQLite

### Frontend
- Vue.js 3
- Vue Router
- Axios
- Vite

---

# Backend Setup

## Step 1: Navigate to backend

```bash
cd backend
```

## Step 2: Create Virtual Environment

```bash
python -m venv venv
```

## Step 3: Activate Virtual Environment

### Windows

```bash
.\venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Step 4: Install Required Packages

```bash
pip install -r backend_requirements.txt
```

## Step 5: Update Requirements File (Optional)

Whenever a new backend package is installed:

```bash
pip freeze > backend_requirements.txt
```

## Step 6: Run Backend

```bash
python app.py
```

Backend runs at:

```
http://127.0.0.1:5000
```

---

# Frontend Setup

## Step 1: Navigate to frontend

```bash
cd frontend
```

## Step 2: Install Dependencies

```bash
npm install
```

## Step 3: Run Frontend

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# Default Admin Account

The application automatically creates a default administrator if one does not already exist.

| Field | Value |
|-------|-------|
| Username | admin |
| Email | admin@trek.com |
| Password | Admin@123 |

---

# Features

- User Registration
- User Login
- JWT Authentication
- Role-Based Authentication
- Admin User Creation
- User Profile API
- Trekker, Staff and Admin Roles

---

# Project Structure

```
backend/
    apis/
    app.py
    models.py
    backend_requirements.txt

frontend/
    src/
    public/
    package.json
    vite.config.js
```

---

# Git Ignore

The following folders are ignored:

- backend/venv
- frontend/node_modules
- __pycache__
- .vscode

---