import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / 'creds.json', "r") as f:
    CREDS = json.load(f)

SECRET_KEY = CREDS.get("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'background_task',
    'api'
]

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

BACKGROUND_TASK_RUN_ASYNC = True

BACKGROUND_TASK_ASYNC_THREADS = 10

MAX_RUN_TIME = 50

MAX_ATTEMPTS = 10 

TIME_ZONE = 'UTC'

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CREDS.get("DB_NAME"),
        'USER': CREDS.get("DB_USER"),
        'PASSWORD': CREDS.get("DB_PASSWORD"),
        'HOST': 'db',
        'PORT': '3306',
    }
}

EMAIL_HOST = CREDS.get("SMTP_HOST")

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST_USER = CREDS.get("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = CREDS.get("EMAIL_HOST_PASSWORD")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'main': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / "logs" / "main.log",
            'formatter': 'standard',
            'maxBytes' : 1024*1024*25, # 25MB
            'backupCount': 100, # 100 max backup files
        },
    },
    'loggers': {
        'api': {
            'handlers': ['main'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

