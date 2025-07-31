#  User_Registeration_management - FastAPI User Registration & Authentication System

A secure, full-stack user authentication and registration system using FastAPI with MongoDB and MySQL.  
It includes login, registration, password change, forgot/reset password, email/phone change, and logout features — with JWT authentication and strong password rules.

---

## Tech Stack

- **Backend Framework**: FastAPI (Python)
- **Databases**:
  - MongoDB (primary user data store)
  - MySQL (secondary for structured reports/logs)
- **Security**:
  - JWT-based Authentication
  - Password Hashing using `bcrypt`
  - Password Expiry (every 30 days)
  - Password Complexity Rules
- **Logging**: All actions are logged in a `.log` file

---

##  Project Structure
```
app/
├── core/
│   ├── security.py           - (token utils here)
│   └── validators.py
├── models/
│   └── request_models.py     - (request models)
├── services/
│   └── user_service.py       - (logic)
├── routes/
│   └── auth_routes.py        - (endpoints)
```

---

##  How to Run This Project

1. Clone the repo

```bash
git clone (Https or SSH)
cd User_Registeration_management
```

---

2.  Create virtual environment and install dependencies

```python
pip install -r requirements.txt
```
3. Start your MongoDB and MySQL servers

```python
Create MySQL DB named user_register


Run run_create_table.py once to create tables
```
4.  Run FastAPI app

```python
uvicorn app.main:app --reload
```
5. Open in browser

```
http://127.0.0.1:8000/
```

**API Endpoints**
```
Method     - Path                     - Description
POST       - /auth/register           - Register new user
POST       - /auth/login              - Login and get JWT token
POST       - /auth/change-password    - Change password (logged-in user)
POST       -/auth/forgot-password     - Send reset link token
POST       - /auth/reset-password     - Reset password using token
POST       - /auth/change-email-phone - Change email or phone number
POST       - /auth/logout             - Logout user (stateless)
```
