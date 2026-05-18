"""
Django settings for stu_back project.
We keep this file simple and add only what our student system needs.
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the student-backend folder (where manage.py lives).
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Basic Django settings ---

SECRET_KEY = "django-insecure-83q#lh$an5+v@(34ut$0=^0=$b+*0hl460qeuq(qk)=4b&i&$o"

DEBUG = True

ALLOWED_HOSTS = []


# --- Installed apps ---
# We register Django's built-in apps plus our students app and API packages.

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party packages for REST API and JWT login
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # Our own app that holds CustomUser and StudentProfile
    "students",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # corsheaders must be placed high so the browser can call our API from React
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "stu_back.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "stu_back.wsgi.application"


# --- Database (SQLite for learning / local development) ---

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --- Tell Django to use our custom user model instead of the default User ---

AUTH_USER_MODEL = "students.CustomUser"


# --- Password validation (Django defaults) ---

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --- Internationalization ---

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

# Django 3.2+ expects this so primary keys use BigAutoField by default.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Django REST Framework settings ---
# By default, every API view requires a logged-in user unless we override it.

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}


# --- Simple JWT settings ---
# Access token is short-lived; refresh token lets the user get a new access token.

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


# --- CORS settings ---
# Allow our React frontend (Vite default port) to call this Django API.

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
