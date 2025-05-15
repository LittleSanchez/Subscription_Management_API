# Optimized Subscription Management API

A RESTful API built with Flask and PostgreSQL for managing user subscriptions.  
Focus: **efficient database queries**, clean architecture, and testability.

---

## 🚀 Features

- ✅ User registration & login (JWT-based)
- ✅ Subscription plan creation & listing (Free, Basic, Pro)
- ✅ Subscribe, cancel, or upgrade user subscription
- ✅ Optimized database queries (with indexing and optional raw SQL)
- ✅ Token blacklisting on logout
- ✅ Pytest-based tests for core functionality

---

## 🛠️ Tech Stack

- Python 3.13+
- Flask
- SQLAlchemy
- PostgreSQL
- Pytest
- JWT (Flask-JWT-Extended)
- Alembic (Flask-Migrate)

---

## ⚙️ Setup Instructions (venv)

```bash
# Clone the repo
git clone https://github.com/LittleSanchez/Subscription_Management_API.git
cd Subscription_Management_API

# Create and activate virtualenv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export FLASK_APP=run.py

# Initialize DB
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the app
flask run