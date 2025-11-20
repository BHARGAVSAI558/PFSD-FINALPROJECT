"""
Django settings for the billingplatform project.
Adjusted for Render deployment: reads secrets from env, supports DATABASE_URL,
adds WhiteNoise for static files and keeps SQLite fallback for local dev.
"""

import os
from pathlib import Path
import dj_database_url

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- Security / env-config ----------
# Use environment variables in production. The fallback values are for local dev only.
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-lakw1()!smzwh)wvzz8gx9mpf+9f&h65%@-by3zv8!^77_0a-^")

# Set DEBUG via env var: "True" or "False"
DEBUG = os.environ.get("DEBUG", "True") == "True"

# ALLOWED_HOSTS should be comma-separated in env, e.g. "example.com,myapp.onrender.com"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ---------- Applications ----------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "billingapp",
    "adminportal",
    "customerportal",
]

# ---------- Middleware ----------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise middleware serves static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "billingplatform.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "billingplatform.wsgi.application"

# ---------- Databases ----------
# Use DATABASE_URL env var (Postgres on Render) if provided; otherwise use local SQLite.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600,
    )
}

# ---------- Password validation ----------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------- Internationalization ----------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------- Static & Media ----------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Keep local static folder for development
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise compressed manifest storage for efficient static serving
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media (user uploaded) - consider S3 in production
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------- Security flags (recommended) ----------
# These are safe to set; if you use local dev with DEBUG=True they won't affect dev.
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "False") == "True"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ---------- Defaults ----------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth redirects (keep your original)
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "customerportal:dashboard"
LOGOUT_REDIRECT_URL = "login"
