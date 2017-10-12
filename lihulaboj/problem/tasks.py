from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Answser
from functools import wraps


def update_answer(fn):
    @wraps(fn)
    def wrapper(answer_id, *args, **kwargs):
        answer = Answser.objects.get(id=answer_id)
        answer.status = 'started'
        answer.save()
        try:
            result = fn(*args, **kwargs)
            answer.result = result
            answer.status = 'finished'
            answer.save()
        except:
            answer.status = 'failed'
            answer.save()
    return wrapper


@shared_task
@update_answer
def judge():
    return 2