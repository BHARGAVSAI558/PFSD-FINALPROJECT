"""
Django settings for the billingplatform project.
Fully configured for Render deployment using SQLite + Whitenoise.
"""

import os
from pathlib import Path

# ---------------- Base Directory ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- Security Keys -----------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-default-key-change-in-production"
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,.onrender.com"
).split(",")

# ---------------- Installed Apps -----------------
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

# ---------------- Middleware ---------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Whitenoise for static files on Render (keep it right after SecurityMiddleware)
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "billingplatform.urls"

# ---------------- Templates ----------------------
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

# ---------------- Database (FOR RENDER: SQLite3) ----------------
# Force SQLite ONLY – no DATABASE_URL override
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------- Password Validation ----------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------- Localization ---------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------- Static Files ----------------------
STATIC_URL = "/static/"
# Where `collectstatic` will gather static files for production (whitenoise serves from here).
STATIC_ROOT = BASE_DIR / "staticfiles"

# Extra static locations during development (your project-level static/ folder)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Whitenoise storage with hashed filenames (good caching). If you get
# manifest errors while debugging, temporarily switch to:
# "whitenoise.storage.CompressedStaticFilesStorage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------- Media Files -----------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------- Security Options -------------------
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------- Authentication Redirects -----------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "customerportal:dashboard"
LOGOUT_REDIRECT_URL = "login"
