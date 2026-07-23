# Trekking Management System (TMS)

The Trekking Management System (TMS) is a full-stack web application developed as part of the **IIT Madras Modern Application Development II (MAD 2)** course.

The application provides a role-based portal for:

- Admin
- Staff
- Trekker

using Flask REST APIs as the backend and Vue.js as the frontend.

---

# Prerequisites

Ensure the following software is installed before running the application:

- Python 3.x
- Node.js (LTS)
- npm
- Git
- Redis
- VS Code (Recommended)

Verify installation:

```bash
python --version
node --version
npm --version
git --version
```

---

# Clone Repository

```bash
git clone <repository-url>

cd Trekking-Management-System
```

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

If the backend starts successfully, the terminal should display:

```
Default Admin Created Successfully.
```

or

```
Default Admin Already Exists.
```

---

# Redis Setup (Required for JWT Blacklisting)

Redis is used to store revoked JWT tokens after user logout.

> **Note:** Redis binaries are not included in this repository. Install Redis separately or use the Redis package provided by the course instructor.

## Step 1: Start Redis Server

Open a new terminal.

Navigate to your Redis installation directory.

```bash
cd <Redis Installation Folder>
```

### Windows

```bash
.\redis-server.exe
```

### Linux / macOS

```bash
redis-server
```

Leave this terminal running.

---

## Step 2: Verify Redis Connection

Open another terminal.

### Windows

```bash
.\redis-cli.exe ping
```

### Linux / macOS

```bash
redis-cli ping
```

Expected Output

```
PONG
```

Redis is now ready for the Flask Backend.

---

# MailHog Setup (Required for Email Testing)

MailHog is used as a local SMTP server for development. All emails sent by the application are captured locally and can be viewed through the MailHog web interface without sending real emails.

> **Note:** MailHog binaries are not included in this repository. Install MailHog separately or use the MailHog package provided by the course instructor.

## Step 1: Start MailHog

Open a new terminal.

Navigate to the MailHog installation directory.

```bash
cd <MailHog Installation Folder>
```

### Windows

```bash
.\MailHog.exe
```

### Linux / macOS

```bash
MailHog
```

Leave this terminal running.

---

## Step 2: Open the MailHog Web Interface

Open your browser and navigate to:

```
http://localhost:8025
```

If MailHog starts successfully, the inbox page will be displayed.

---

## Step 3: Verify Email Delivery

After creating a new Staff account from the Admin Portal:

- A welcome email will be sent automatically.
- Open the MailHog Web Interface.
- Verify that the welcome email appears in the inbox.

If emails are not received:

- Ensure MailHog is running.
- Verify the SMTP configuration in `backend/utils/mail.py`.
- Check the Flask backend terminal for email-related errors.

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

# Running the Complete Application

Open **three terminals**.

### Terminal 1

Run Backend

```bash
cd backend

.\venv\Scripts\activate

python app.py
```

---

### Terminal 2

Run Redis

```bash
redis-server
```

or

```bash
.\redis-server.exe
```

---

### Terminal 3

Run Frontend

```bash
cd frontend

npm install

npm run dev
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

### Authentication

- User Registration
- User Login
- JWT Authentication
- JWT Token Blacklisting
- Role-Based Authentication

### Admin

- Automatic Default Admin Creation
- Create Staff
- Role Based Access

### Profile

- View Profile
- Update Profile
- Change Password

### Frontend

- Vue Router
- Axios Integration
- Responsive User Interface

---

# Tech Stack

## Backend

- Python
- Flask
- Flask RESTful
- Flask SQLAlchemy
- Flask JWT Extended
- Flask CORS
- SQLite
- Redis

## Frontend

- Vue.js 3
- Vue Router
- Axios
- Vite

---

# Configuration

Current configuration is available in:

```
backend/app.py
```

Update when required:

- JWT_SECRET_KEY
- SQLAlchemy Database URI
- Redis Configuration

---

# Git Ignore

The following folders/files are ignored:

- backend/venv
- frontend/node_modules
- __pycache__
- .vscode
- .env
- *.sqlite3
- *.db
- instance/

---