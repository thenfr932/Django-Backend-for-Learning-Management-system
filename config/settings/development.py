"""
Development-specific Django settings.
Use with: DJANGO_SETTINGS_MODULE=config.settings.development
"""

from .base import *  # noqa: F401, F403

# --- Debug ---
DEBUG = True

# --- Database (SQLite for local dev) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- CORS (permissive for local dev) ---
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# --- Cookies (relaxed for HTTP local dev) ---
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# --- Hosts ---
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# --- Static files (no compression in dev) ---
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
