"""
Django 5.0.1
"""

from pathlib import Path
from os import getenv

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_DIR = Path(getenv("STATE_DIR", BASE_DIR))

SECRET_KEY_FILE = getenv("SECRET_KEY_FILE")
if SECRET_KEY_FILE is None:
    SECRET_KEY = "django-insecure-@dl&bssqzr%xaviwu73kb!bng!(sgx#^u0+q7!$_&=kw+*4$#z"
else:
    with open(SECRET_KEY_FILE) as f:
        SECRET_KEY = f.read()

DEBUG = getenv("DEBUG", "True").lower() in ["true", "1", "yes"]

SCHEME = getenv("SCHEME", "http")
ALLOWED_HOSTS = getenv("HOST", "localhost").split(",")
CSRF_TRUSTED_ORIGINS = [f"{SCHEME}://{host}" for host in ALLOWED_HOSTS]

APP_ROOT = getenv("APP_ROOT", "")

INSTALLED_APPS = [
    "api.apps.ApiConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "app.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": STATE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = APP_ROOT + "static/"
STATIC_ROOT = getenv("STATIC_ROOT")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
