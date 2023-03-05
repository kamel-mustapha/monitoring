from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-cp3%&%3l1xm_)_ig%40i6&64ddrl_mvx4#wpy6pe5d@f!d5i7$'

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
        'NAME': 'monitoring',
        'USER': 'musk',
        'PASSWORD': 'musk',
        'HOST': 'db',
        'PORT': '3306',
    }
}

EMAIL_HOST = "smtp.gmail.com"

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST_USER = "musk96.km@gmail.com"

EMAIL_HOST_PASSWORD = "eacfvajdbpzoannp"

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

