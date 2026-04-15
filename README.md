# Django Backend for Learning Mangement System

A Django-based backend for the InternGrad platform, providing APIs for course management, user accounts, enrollments, and payments.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
- [Running the Server](#running-the-server)
- [Project Structure](#project-structure)
- [Available Endpoints](#available-endpoints)

## Project Overview

This is a Django REST Framework application that manages:

- **Accounts**: User registration and authentication
- **Courses**: Course management and lessons
- **Enrollments**: Student enrollments in courses
- **Payments**: Payment processing for course access

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **pip** (comes with Python)

## Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/thenfr932/Django-Backend-for-Learning-Management-system.git
cd Django-Backend-for-Learning-Management-system
```

### 2. Create a Virtual Environment

A virtual environment isolates project dependencies from your system Python.

**On Windows (PowerShell/CMD):**

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Once activated, your terminal prompt should show `(.venv)` prefix.

### 3. Install Dependencies

With the virtual environment activated, install required packages:

```bash
pip install --upgrade pip
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt python-dotenv
```

**Alternative**: If a `requirements.txt` file exists, use:

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

Initialize the database schema:

```bash
python manage.py migrate
```

This command:

- Applies all pending database migrations
- Creates tables for users, courses, enrollments, and payments
- Sets up the SQLite database (`db.sqlite3`)

### 5. Create a Superuser (Admin Account)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:

- Username
- Email
- Password

### 6. (Optional) Load Sample Data

If sample data fixtures exist, you can load them:

```bash
python manage.py loaddata <fixture-name>
```

## Running the Server

### Start the Development Server

With the virtual environment activated, run:

```bash
python manage.py runserver
```

Expected output:

```
Starting development server at http://127.0.0.1:8000/
```

**Access the server:**

- **API Root**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  - Login with the superuser credentials created earlier

### Run on a Specific Port

To run on a different port:

```bash
python manage.py runserver 0.0.0.0:8080
```

### Stop the Server

Press `Ctrl+C` in the terminal to stop the development server.

## Project Structure

```
Django-Backend-for-Learning-Management-system/
├── accounts/              # User authentication and profile management
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── migrations/
├── courses/               # Course and lesson management
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── migrations/
├── enrollments/           # Student course enrollments
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── migrations/
├── payments/              # Payment processing
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── migrations/
├── config/                # Django settings and URL routing
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database (auto-generated)
└── README.md
```

## Available Endpoints

### Accounts

- `POST /accounts/register/` - Register a new user
- `POST /accounts/login/` - User login
- `GET /accounts/profile/` - Get current user profile
- `PUT /accounts/profile/` - Update user profile

### Courses

- `GET /courses/` - List all courses
- `POST /courses/` - Create a new course (admin only)
- `GET /courses/<id>/` - Get course details
- `GET /courses/<id>/lessons/` - Get lessons for a course

### Enrollments

- `GET /enrollments/` - List user enrollments
- `POST /enrollments/` - Enroll in a course
- `GET /enrollments/<id>/` - Get enrollment details

### Payments

- `GET /payments/` - List payment transactions
- `POST /payments/` - Create a payment
- `GET /payments/<id>/` - Get payment details

## Troubleshooting

### Virtual Environment Not Activating

- Ensure Python is installed correctly
- Use the full path to activate: `path\to\.venv\Scripts\Activate.ps1`

### Database Migration Errors

- Delete `db.sqlite3` and all migration files except `__init__.py`
- Run `python manage.py makemigrations` then `python manage.py migrate`

### Module Not Found Errors

- Verify virtual environment is activated
- Run `pip install -r requirements.txt` or install packages individually

### Port Already in Use

- Use a different port: `python manage.py runserver 8080`
- Or kill the process using port 8000

## Development Notes

- The project uses **SQLite** by default for development
- Debug mode is enabled (`DEBUG = True` in settings.py)
- Never use debug mode in production
- Sensitive credentials should be stored in environment variables

---

For more information, visit the [Django Documentation](https://docs.djangoproject.com/)
