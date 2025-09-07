import json
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load configuration from JSON
CONFIG_PATH = BASE_DIR / 'config.json'

try:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {}

# Security
SECRET_KEY = config.get("SECRET_KEY")
DEBUG = config.get("DEBUG", True)
ALLOWED_HOSTS = config.get("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])

# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "django_celery_results",
    # Local apps
    "bot",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL configuration
ROOT_URLCONF = "TGSaleDB.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# Database
db_config = config.get("DATABASE", {})
DATABASES = {
    'default': {
        'ENGINE': db_config.get('ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / db_config.get('NAME', 'db.sqlite3'),
        'USER': db_config.get('USER', ''),
        'PASSWORD': db_config.get('PASSWORD', ''),
        'HOST': db_config.get('HOST', ''),
        'PORT': db_config.get('PORT', ''),
    }
}

# For PostgreSQL (alternative using DATABASE_URL)
if config.get("DATABASE_URL"):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        default=config.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    )

# Celery settings
celery_config = config.get("CELERY", {})
CELERY_BROKER_URL = config.get("REDIS_URL", celery_config.get("BROKER_URL", "redis://localhost:6379/0"))
CELERY_RESULT_BACKEND = celery_config.get("RESULT_BACKEND", "django-db")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Telegram settings
telegram_config = config.get("TELEGRAM", {})
TELEGRAM_BOT_TOKEN = "8377138702:AAHIC2T-Ubzz5ScA2CCRyJSC1RTu9_McyzY" #telegram_config.get("BOT_TOKEN", "")
ADMIN_CHAT_IDS = telegram_config.get("ADMIN_CHAT_IDS", [])

# Static and media files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Internationalization
LANGUAGE_CODE = config.get("LANGUAGE_CODE", "ru-ru")
TIME_ZONE = config.get("TIME_ZONE", "Europe/Moscow")
USE_I18N = True
USE_TZ = True

# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
