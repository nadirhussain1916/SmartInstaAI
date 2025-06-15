# SmartInstaAI Backend Setup Guide

This guide provides step-by-step instructions to set up, run, and test the Django backend for SmartInstaAI.

---

## 1. Requirements

- **Python Version:** 3.11 or 3.12 recommended (compatible with Django 5.2.3)
- **MySQL Version:** 8.x (or compatible with `mysqlclient`)
- **pip** (Python package manager)

---

## 2. Python Installation

- Download Python from the [official website](https://www.python.org/downloads/).
- During installation, check **"Add Python to PATH"**.
- Verify installation:
  ```powershell
  python --version
  pip --version
  ```

---

## 3. Create & Activate Virtual Environment

From the `backend` directory:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

---

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 5. MySQL Database Setup

- **Install MySQL**: [Download MySQL](https://dev.mysql.com/downloads/installer/)
- **Create Database:**
  1. Open MySQL command line or MySQL Workbench.
  2. Run:
     ```sql
     CREATE DATABASE instagram;
     ```
- **Database Credentials:**
  - User: `root`
  - Password: `1234`
  - Host: `localhost`
  - Port: `3308`
  - (Edit `backend/instagram_auth/settings.py` if you use different credentials)

---

## 6. Django Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

## 7. Run the Development Server

```powershell
python manage.py runserver
```
- The server will be available at: http://127.0.0.1:8000

---

## 8. API Endpoints & Testing

### Authentication
- **Sign In:**
  - `POST /instagram/signin-user/`
  - **Body:**
    ```json
    { "username": "<your_username>", "password": "<your_password>" }
    ```
  - **Response:** JWT `access` and `refresh` tokens

- **Refresh Token:**
  - `POST /instagram/signin-user/refresh/`
  - **Body:**
    ```json
    { "refresh": "<refresh_token>" }
    ```

### Instagram Profile Fetch
- **Fetch Profile:**
  - `POST /instagram/get-instagram-user/`
  - **Body:**
    ```json
    { "username": "<instagram_username>" }
    ```
  - **Response:** Profile data (username, full name, followers, posts, profile_pic)

### Fetch & Save User Data (Requires Auth)
- **Fetch & Save:**
  - `POST /instagram/fetch-userData/`
  - **Headers:**
    - `Authorization: Bearer <access_token>`
  - **Body:** _Empty_
  - **Response:** Success message

---

## 9. Example API Test with curl

```powershell
# Sign in and get tokens
curl -X POST http://127.0.0.1:8000/instagram/signin-user/ -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"testpass\"}"

# Fetch Instagram profile
curl -X POST http://127.0.0.1:8000/instagram/get-instagram-user/ -H "Content-Type: application/json" -d "{\"username\": \"cristiano\"}"

# Fetch and save user data (requires access token)
curl -X POST http://127.0.0.1:8000/instagram/fetch-userData/ -H "Authorization: Bearer <access_token>"
```

---

## 10. Notes
- **Media Files:** Profile images are saved in `backend/media/instagram/`.
- **CORS:** For frontend integration, update `ALLOWED_HOSTS` and CORS settings in `settings.py` as needed.
- **Port:** Default Django port is `8000`. Change with `python manage.py runserver 0.0.0.0:<port>` if needed.

---

## 11. Troubleshooting
- Ensure MySQL is running and accessible on the configured port.
- If you change DB credentials, update them in `backend/instagram_auth/settings.py`.
- For any Python or pip errors, ensure your virtual environment is activated.

---

## 12. Author
Developed by Muhammad Bilal
