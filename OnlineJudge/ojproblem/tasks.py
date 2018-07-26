from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import *
from functools import wraps
import json
import time


def update_answer(fn):
    @wraps(fn)
    def wrapper(answer_id, *args, **kwargs):
        result = fn(*args, **kwargs)
        print result
    return wrapper


@shared_task
@update_answer
def judge(source_code):
    from .submittasks import judgeOne
    testin = 'world'
    testout = 'hello world\n'
    script = '''
print('hello world')
'''
    res = judgeOne.delay(testin, testout, script)
    while not res.ready():
        time.sleep(0.5)
    print res.result
    return res.result