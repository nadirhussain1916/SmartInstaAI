Related Doc:
https://developers.facebook.com/docs/instagram-platform/overview#features-and-permissions

# 📸 Instagram Profile Fetcher API (Django + DRF)

A Django REST Framework-based API that retrieves Instagram user profile data (username, full name, follower count, post count, and profile image) using the `instaloader` library. This project also includes secure user authentication with JWT (sign-up, login, and token refresh support), making it easy to integrate into modern frontend applications such as React.

---

## 🚀 Features

- 🔐 **JWT Authentication** — Register and login endpoints with secure access/refresh token generation.
- 🔍 **Instagram Profile Lookup** — Fetch public user data using a valid Instagram username.
- 🖼️ **Profile Picture Handling** — Automatically downloads and stores profile images.
- 🛡️ **Error Handling** — Graceful API responses for invalid usernames and external service failures (like Instagram rate limits or 401 errors).
- ⚙️ **Frontend-Ready** — Easily integrate with frontend frameworks like React or Vue.

---

## 📦 Installation

### 1. Install Requirements

Run the following command from your project root to install all dependencies:

```bash
pip install -r requirements.txt


### 🛠️ Setup & Configuration
2. Apply Migrations
Run the following commands to set up the database:

python manage.py makemigrations
python manage.py migrate


3. Run Development Server
Start the Django server locally:
python manage.py runserver
Server will be available at: http://127.0.0.1:8000


🔌 API Endpoints
Method	Endpoint	Description
POST	http://127.0.0.1:8000/instagram/get-instagram-user/	Fetch Instagram profile data
POST	http://127.0.0.1:8000/instagram/signup-user/	Register new Django user from IG profile
POST	http://127.0.0.1:8000/instagram/signin-user/ Login and receive JWT tokens
POST	http://127.0.0.1:8000/instagram/signin-user/refresh/	Refresh expired access token


⚙️ Frontend Integration
If you're using React or another frontend framework served on a different host/port, update the following settings in your Django settings.py:

ALLOWED_HOSTS = ['*']  # Or specify your domain/frontend IP

INSTALLED_APPS += ['corsheaders']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# Allow all origins (for development only)
CORS_ALLOW_ALL_ORIGINS = True


📁 Project Structure
instagram_api/
├── api/                    # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── media/                  # Stored profile images
├── requirements.txt
├── manage.py
└── README.md


👨‍💻 Author
Developed by Muhammad Bilal 
