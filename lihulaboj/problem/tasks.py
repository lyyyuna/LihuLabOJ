from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Answser
from functools import wraps
from .languageconf import *
import requests, os, hashlib


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
        except Exception as e:
            print (e)
            answer.status = 'failed'
            answer.save()
    return wrapper


@shared_task
@update_answer
def judge(source_code, language, max_cpu_time, max_memory, test_case_id):
    token = os.environ.get('JUDGE_TOKEN')
    headers = {'X-Judge-Server-Token' : hashlib.sha256(token.encode('utf-8')).hexdigest()}

    judge_server_ip = os.environ.get('JUDGE_SERVER_IP')
    judge_server_port = os.environ.get('JUDGE_SERVER_PORT')
    judge_server_url = 'http://%s:%s/judge' % (judge_server_ip, judge_server_port)
    
    args = {
        'src' : source_code,
        'language_config' : lang_config[language], # if not predefined lang, raise exception
        'max_cpu_time' : max_cpu_time,
        'max_memory' : max_memory,
        'test_case_id' : test_case_id,
        'output' : False
    }

    r = requests.post(url=judge_server_url, headers=headers, json=args)
    return r.text