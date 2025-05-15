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

docker compose up # Or docker-compose up
```
