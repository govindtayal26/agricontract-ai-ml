"""
Django settings for agricontract_project.

Supports:
- Local development
- Render deployment
- SQLite locally
- PostgreSQL on Render
- WhiteNoise static files
"""

from pathlib import Path
import os

import dj_database_url


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-development-only-secret-key-change-me"
)

DEBUG = os.environ.get(
    "DEBUG",
    "True"
).lower() == "true"


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# Render automatically provides this variable.
render_hostname = os.environ.get(
    "RENDER_EXTERNAL_HOSTNAME"
)

if render_hostname:
    ALLOWED_HOSTS.append(
        render_hostname
    )

# Optional additional hosts.
#
# Example:
# ALLOWED_HOSTS_EXTRA=example.com,www.example.com

extra_hosts = os.environ.get(
    "ALLOWED_HOSTS_EXTRA",
    ""
)

if extra_hosts:
    ALLOWED_HOSTS.extend(
        host.strip()
        for host in extra_hosts.split(",")
        if host.strip()
    )


# ============================================================
# CSRF TRUSTED ORIGINS
# ============================================================

CSRF_TRUSTED_ORIGINS = []

if render_hostname:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{render_hostname}"
    )

# Optional custom domains/origins.
#
# Example:
# CSRF_TRUSTED_ORIGINS_EXTRA=https://example.com,https://www.example.com

extra_origins = os.environ.get(
    "CSRF_TRUSTED_ORIGINS_EXTRA",
    ""
)

if extra_origins:
    CSRF_TRUSTED_ORIGINS.extend(
        origin.strip()
        for origin in extra_origins.split(",")
        if origin.strip()
    )


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project application
    "marketplace",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise serves static files in production.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = (
    "agricontract_project.urls"
)


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [

    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.debug",

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = (
    "agricontract_project.wsgi.application"
)


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.environ.get(
    "DATABASE_URL"
)

if DATABASE_URL:

    # --------------------------------------------------------
    # Production: PostgreSQL
    # --------------------------------------------------------

    DATABASES = {

        "default": dj_database_url.parse(

            DATABASE_URL,

            conn_max_age=600,

            conn_health_checks=True,
        )
    }

else:

    # --------------------------------------------------------
    # Local development: SQLite
    # --------------------------------------------------------

    DATABASES = {

        "default": {

            "ENGINE":
                "django.db.backends.sqlite3",

            "NAME":
                BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

# Source static directory.
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Collected static files for production.
STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)


# ============================================================
# WHITENOISE
# ============================================================

STORAGES = {

    # User-uploaded files / default storage
    "default": {
        "BACKEND":
            "django.core.files.storage.FileSystemStorage",
    },

    # Static files
    "staticfiles": {
        "BACKEND":
            "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = (
    BASE_DIR / "media"
)


# ============================================================
# AUTHENTICATION
# ============================================================

# Your normal application login is handled from the home page.
LOGIN_URL = "home"

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "home"


# ============================================================
# SECURITY SETTINGS
# ============================================================

if not DEBUG:

    # --------------------------------------------------------
    # Render / production HTTPS configuration
    # --------------------------------------------------------

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    # Secure session cookie.
    SESSION_COOKIE_SECURE = True

    # Secure CSRF cookie.
    CSRF_COOKIE_SECURE = True

    # Redirect HTTP → HTTPS.
    SECURE_SSL_REDIRECT = True

    # HTTP Strict Transport Security.
    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

    # Prevent MIME-type sniffing.
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Prevent the site from being embedded in frames.
    X_FRAME_OPTIONS = "DENY"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)