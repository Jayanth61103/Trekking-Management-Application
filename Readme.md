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
- MailHog
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

## Step 3.5: Create Environment File

Create a `.env` file inside the `backend` folder with the following:

```
JWT_SECRET_KEY=your_secret_key_here
```

This file is excluded from Git via `.gitignore` and must be created manually after cloning.

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

# Redis Setup (Required for JWT Blacklisting, Celery Broker, and Caching)

Redis is used for three purposes in this application:

- Storing revoked JWT tokens after user logout (Database 0)
- Acting as the message broker and result backend for Celery (Database 1)
- Caching frequently accessed API responses, such as Trek listings (Database 1)

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

# Celery Setup (Required for Background Jobs and Scheduled Tasks)

Celery is used to run background jobs outside the normal request/response cycle, such as sending reminder emails, generating monthly reports, and exporting trekking history as CSV. Celery Beat is used to automatically trigger the scheduled jobs (daily reminders and the monthly report) on a timer.

Celery requires Redis to already be running, since Redis acts as its message broker (see Redis Setup above).

> **Note:** On Windows, Celery's default worker pool is not fully compatible, so the `--pool=solo` flag is required.

## Step 1: Start the Celery Worker

Open a new terminal.

```bash
cd backend

.\venv\Scripts\activate

celery -A tasks worker --pool=solo --loglevel=info
```

If successful, the terminal will list the registered tasks (`tasks.export_trekking_history_csv`, `tasks.generate_monthly_report`, `tasks.send_trek_reminders`) and end with a line similar to:

```
celery@YOUR-PC-NAME ready.
```

Leave this terminal running.

---

## Step 2: Start Celery Beat

Open another new terminal.

```bash
cd backend

.\venv\Scripts\activate

celery -A tasks beat --loglevel=info
```

If successful, the terminal will display the broker configuration and begin logging scheduler activity.

Leave this terminal running.

---

## Step 3: Verify Celery is Working

Open a temporary terminal.

```bash
cd backend

.\venv\Scripts\activate

python
```

Inside the Python shell:

```python
from tasks import generate_monthly_report
generate_monthly_report.delay()
exit()
```

Check the Celery Worker terminal — it should log that it received and executed the task within a few seconds. Then check the MailHog Web Interface (`http://localhost:8025`) for the report email.

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

Open **six terminals**.

---

### Terminal 1 - Backend

Run the Flask Backend.

```bash
cd backend

.\venv\Scripts\activate

python app.py
```

Backend URL:

```
http://127.0.0.1:5000
```

---

### Terminal 2 - Redis Server

Start the Redis Server.

```bash
redis-server
```

or

```bash
.\redis-server.exe
```

Leave this terminal running.

**Optional: Verify Redis Connection**

Open a **new terminal** only if you want to verify that Redis is running correctly.

Windows:

```bash
.\redis-cli.exe ping
```

Linux / macOS:

```bash
redis-cli ping
```

Expected Output:

```
PONG
```

---

### Terminal 3 - MailHog

Navigate to the MailHog installation directory.

```bash
.\MailHog.exe
```

Leave this terminal running.

Open the MailHog Web Interface:

```
http://localhost:8025
```

---

### Terminal 4 - Celery Worker

```bash
cd backend

.\venv\Scripts\activate

celery -A tasks worker --pool=solo --loglevel=info
```

Leave this terminal running.

---

### Terminal 5 - Celery Beat

```bash
cd backend

.\venv\Scripts\activate

celery -A tasks beat --loglevel=info
```

Leave this terminal running.

---

### Terminal 6 - Frontend

Run the Vue Frontend.

```bash
cd frontend

npm install

npm run dev
```

Frontend URL:

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
- Manage Treks (Create, Update, Assign Guide)
- Manage Trekkers (View, Search, Blacklist/Deactivate)
- View All Booking Records (History)
- Dashboard Statistics

### Staff

- View Assigned Treks Only
- Update Available Trek Slots
- Update Trek Status (Open / Completed / Cancelled)
- View and Manage Participant List

### Trekker

- Browse and Filter Open Treks (Difficulty, Location, Duration)
- Book Treks with Slot and Duplicate-Booking Validation
- View and Cancel My Bookings
- Export Trekking History as CSV (via Email)

### Profile

- View Profile
- Update Profile
- Change Password

### Frontend

- Vue Router (Modular Route Files per Role)
- Axios Integration
- Responsive User Interface

### Background Jobs (Celery + Redis)

- Daily Trek Reminder Emails (Celery Beat, Scheduled)
- Monthly Trekking Activity Report (Celery Beat, Scheduled)
- User-Triggered CSV Export of Trekking History (Async, Emailed on Completion)

### Caching (Redis)

- Cached Trek Listing Endpoint with Automatic Invalidation on Trek/Booking Changes

### Mailing 

- Staff Welcome Email (Development using MailHog)
- Trek Reminder Emails
- Monthly Report Emails
- Trekking History CSV Export Emails

---

# Tech Stack

## Backend

- Python
- Flask
- Flask RESTful
- Flask SQLAlchemy
- Flask JWT Extended
- Flask CORS
- Flask Mail
- Celery
- Redis
- SQLite

## Development Tools

- Redis
- MailHog
- Git

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
- Mail Server Configuration

Celery-specific configuration (broker URL, result backend, and scheduled task timings) is available in:

```
backend/celery_app.py
```

---

# Known Limitations & Design Decisions

- **Trek status flow**: Uses the existing `Upcoming → Open → Full/Completed/Cancelled` states to represent the "started/ongoing/completed" lifecycle described in the project brief, rather than introducing additional enum values, to avoid schema migrations under the project timeline.
- **Booking approval**: Bookings are automatically approved on creation (subject to slot availability and duplicate-booking checks) rather than requiring manual Admin/Staff approval, since the brief does not specify an approval workflow.
- **Password reset via email**: Not implemented; only the Staff welcome email, reminder, report, and CSV export flows use MailHog.
- **CSV export delivery**: The exported trekking history is emailed as an attachment rather than offered as a direct in-browser download, since the export runs asynchronously via Celery outside the request/response cycle.
- **Cache TTL**: Trek listings are cached for 60 seconds and are explicitly invalidated whenever a Trek is created, updated, booked, or cancelled, to balance performance with data freshness.
- **Testing**: No automated test suite; testing was performed manually per milestone.

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
- celerybeat-schedule
- celerybeat-schedule-shm
- celerybeat-schedule-wal
- dump.rdb