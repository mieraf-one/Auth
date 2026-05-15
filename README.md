# 🔐 FastAPI Auth Service

A production-ready authentication system built with FastAPI, PostgreSQL, and JWT.

---

## 🚀 Features

- User registration and login
- JWT access token + refresh token system
- Email verification with OTP code
- Forgot password / reset password flow
- Update email, username, and password
- Soft delete account
- Rate limiting on email sending (1 minute cooldown)
- Role-based access control (user / admin)
- Secure password hashing with bcrypt
- Environment-based configuration

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| FastAPI | Web framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| Pydantic v2 | Data validation |
| python-jose | JWT encoding/decoding |
| bcrypt | Password hashing |
| fastapi-mail | Email sending |
| pydantic-settings | Environment variable management |

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py           # Environment settings
│   │   └── security.py         # JWT and password hashing
│   ├── dependencies/
│   │   └── auth.py             # get_current_user dependency
│   ├── models/
│   │   ├── user.py
│   │   ├── refresh_token.py
│   │   └── emailCode.py
│   ├── schemas/
│   │   └── auth.py             # Pydantic schemas
│   ├── services/
│   │   └── auth/               # Business logic
│   ├── routers/
│   │   └── auth.py             # API endpoints
│   ├── database.py
│   └── main.py
├── alembic/
│   ├── versions/
│   └── env.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/mieraf-one/Auth.git
cd Auth/backend
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Then fill in your `.env` file:

```env
SECRET_KEY=your_super_secret_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/authdb
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
```

To generate a secure `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`

Interactive docs at `http://localhost:8000/docs`

---

## 📌 API Endpoints

### Auth

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|-----------|
| POST | `/auth/signup` | Register a new user | ❌ |
| POST | `/auth/login` | Login and get tokens | ❌ |
| DELETE | `/auth/logout` | Logout and revoke refresh token | ✅ |
| POST | `/auth/refresh` | Get new access token | ❌ |
| GET | `/auth/me` | Get current user profile | ✅ |

### Email Verification

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|-----------|
| POST | `/auth/send-code` | Send verification code to email | ✅ |
| POST | `/auth/verify` | Verify email with code | ✅ |

### Forgot Password

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|-----------|
| POST | `/auth/reset-code` | Send password reset code | ✅ |
| POST | `/auth/forgot-password` | Reset password with code | ✅ |

### Account Management

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|-----------|
| POST | `/auth/password/update` | Update password | ✅ |
| POST | `/auth/email/update` | Update email | ✅ |
| POST | `/auth/username/update` | Update username | ✅ |
| DELETE | `/auth/delete-account` | Soft delete account | ✅ |

---

## 🔑 Authentication

This API uses **Bearer token** authentication.

After login, include the access token in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

Access tokens expire in **15 minutes**. Use the `/auth/refresh` endpoint with your refresh token to get a new one.

---

## 🔒 Security Features

- Passwords hashed with **bcrypt**
- JWT tokens signed with **HS256**
- Refresh tokens stored in database and revoked on logout
- Same error message for wrong email and wrong password (prevents user enumeration)
- OTP codes generated with `secrets` module (cryptographically secure)
- Rate limiting: 1 minute cooldown between verification code requests
- Inactive accounts blocked from all protected endpoints

---

## 📧 Email Setup (Gmail)

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account → Security → App Passwords
3. Generate an app password
4. Use that password as `MAIL_PASSWORD` in your `.env`

---

## 🗃️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT signing key | ✅ |
| `DATABASE_URL` | PostgreSQL connection URL | ✅ |
| `MAIL_USERNAME` | Gmail address | ✅ |
| `MAIL_PASSWORD` | Gmail app password | ✅ |
| `MAIL_FROM` | Sender email address | ✅ |

---

## 📄 License

MIT
