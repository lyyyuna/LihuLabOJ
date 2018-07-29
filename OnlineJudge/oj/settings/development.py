from .base import *

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@ee+ba*4l6_9&s4tg!8uoi140xz%2lkk(y%x&aqtirbd!lv1_^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_ENV_DB', 'ojtest'),
        'USER': os.environ.get('DB_ENV_POSTGRES_USER', 'yiyangli'),
        'PASSWORD': os.environ.get('DB_ENV_POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('DB_ENV_ADDR', '127.0.0.1'),
        'PORT': os.environ.get('DB_ENV_PORT', '5432'),
        'CONN_MAX_AGE' : 0,
    },
}

rabbituser = os.environ.get('RABBIT_USER')
rabbitpass = os.environ.get('RABBIT_PASS')
rabbithost = os.environ.get('RABBIT_HOST')
rabbitport = os.environ.get('RABBIT_PORT')
rabbitvhost = os.environ.get('RABBIT_VHOST2')
CELERY_BROKER_URL  = 'amqp://{}:{}@{}:{}/{}'.format(rabbituser, rabbitpass, rabbithost, rabbitport, rabbitvhost)

CELERY_RESULT_BACKEND = 'rpc://'
# CELERY_REDIS_MAX_CONNECTIONS = 2
CELERY_TASK_RESULT_EXPIRES = 300
CELERYD_MAX_TASKS_PER_CHILD = 100