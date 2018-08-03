from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


app = Celery('lihulaboj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_transport_options = {
    'max_retries': 0,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}
app.autodiscover_tasks()