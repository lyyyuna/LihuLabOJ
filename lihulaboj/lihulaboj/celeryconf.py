from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


app = Celery('lihulaboj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()