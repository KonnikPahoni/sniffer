import sys
import logging
import os
import django
from environs import Env

sys.dont_write_bytecode = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa"

if os.path.exists(os.path.join(BASE_DIR, ".env")):
    env = Env()
    env.read_env(os.path.join(BASE_DIR, ".env"))

# if os.path.exists(os.path.join(BASE_DIR, ".env.local")):
#     env = Env()
#     env.read_env(os.path.join(BASE_DIR, ".env.local"))

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TIMEZONE = 'UTC'

TIME_ZONE = 'UTC'

BACKUP_DISTANCE = os.environ['BACKUP_DISTANCE']
BUCKET_NAME = os.environ['BUCKET_NAME']
SPACES_ENDPOINT_URL = os.environ['SPACES_ENDPOINT_URL']
REGION_NAME = os.environ['REGION_NAME']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': 5432
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', os.environ['APP_HOST']]

if not os.path.isdir(os.path.join(BASE_DIR, 'var')):
    os.mkdir(os.path.join(BASE_DIR, 'var'))

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_BOT_ID = os.environ['TELEGRAM_BOT_ID']

HEALTH_CHECK_INTERVAL = 5
SCHEDULER_NAME = "Scheduler"
APP_CORE_NAME = "AppCore"

CONFIGURED_THREADS = [APP_CORE_NAME,
                      SCHEDULER_NAME,
                      'MainThread',
                      'APScheduler',
                      'Bot:' + str(TELEGRAM_BOT_ID) + ':dispatcher',
                      'Bot:' + str(TELEGRAM_BOT_ID) + ':updater']

REQUEST_TIMEOUT = 10
TICKER_INTERVAL = 60

PATH_TO_LOGS = 'var/horseshoe.log'
LOGGING_LEVEL_CONSOLE = logging.DEBUG
LOGGING_LEVEL_FILE = logging.INFO
LOGGING_LEVEL_TELEGRAM = logging.INFO

INSTALLED_APPS = ("data_getter", "django_celery_beat",)

DEBUG = True

django.setup()
