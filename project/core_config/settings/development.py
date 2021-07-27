"""Development/local envs.

Decouple always searches for Options in this order:
 - Environment variables;
 - Repository: ini or .env file;
 - default argument passed to config.
"""
from pathlib import Path

import dj_database_url
from celery.schedules import crontab
from decouple import Csv, AutoConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

config = AutoConfig(search_path=ENV_BASE_DIR / 'deploy/dev/.env')

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default=f'sqlite:///{str(BASE_DIR)}/db.sqlite3',
        cast=dj_database_url.parse
    )
}

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Email sending
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
DEFAULT_FROM_EMAIL = 'admin@dj_demo_app.com'
ADMINS = [("testuser", "test.user@email.com"), ]

# Celery Configuration Options
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "blog.tasks.sample_task",
        "schedule": crontab(minute="*/3"),  # run once every 3 mins
    },
    "sends_to_telegram": {
        "task": "blog.tasks.post_unpublished_to_telegram",
        "schedule": crontab(minute="*/10"),
    },
}


TELEGRAM_API = {
    'bot_token': config('TELEGRAM_API_BOT_TOKEN'),
    'channel_name': 'djcelery',
}
