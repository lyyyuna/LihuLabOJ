from .base import *

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@ee+ba*4l6_9&s4tg!8uoi140xz%2lkk(y%x&aqtirbd!lv1_^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_ENV_DB', 'postgres'),
        'USER': os.environ.get('DB_ENV_POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_ENV_POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_PORT_5432_TCP_ADDR', 'db'),
        'PORT': os.environ.get('DB_PORT_5432_TCP_PORT', ''),
    },
}

REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')

CELERY_BROKER_URL = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT,REDIS_DB)

CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT,REDIS_DB)
CELERY_REDIS_MAX_CONNECTIONS = 2
CELERY_TASK_RESULT_EXPIRES = 300