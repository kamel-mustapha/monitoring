import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / 'creds.json', "r") as f:
    CREDS = json.load(f)

SECRET_KEY = CREDS.get("SECRET_KEY")

DEBUG = CREDS.get("DEBUG")

ALLOWED_HOSTS = CREDS.get("ALLOWED_HOSTS")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
    'corsheaders',
    'tailwind',
    'theme',
    'website',
    'django_browser_reload',
    'task',
    'payment'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'api.middleware.KeyLogin',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'angularoutput'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / "db.sqlite3"
#         }
#     }
# else:
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


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'website.forms.MaximumLengthValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "website.User"

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [BASE_DIR / 'staticfiles']

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAILWIND_APP_NAME = 'theme'

TAILWIND_CSS_PATH = 'tailwind.css'
import os

INTERNAL_IPS = [
    "127.0.0.1",
]

# SMTP
EMAIL_HOST = CREDS.get("SMTP_HOST")

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST_USER = CREDS.get("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = CREDS.get("EMAIL_HOST_PASSWORD")

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

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
        },
        'website': {
            'handlers': ['main'],
            'level': 'INFO',
            'propagate': True,
        },
        'payment': {
            'handlers': ['main'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}


CSRF_TRUSTED_ORIGINS = ["https://statuschecks.net", "https://www.statuschecks.net"]