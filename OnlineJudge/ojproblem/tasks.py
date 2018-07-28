from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.result import allow_join_result
from .models import *
from functools import wraps
import json
import time
from ojuser.models import *
from django.contrib.auth.models import User


def update_answer(fn):
    @wraps(fn)
    def wrapper(answer_id, problem_id, owner_id, *args, **kwargs):
        answer = OJAnswer.objects.get(id=answer_id)
        p = OJProblem.objects.get(id=problem_id)
        owner = User.objects.get(id=owner_id)

        answer.status = 'started'
        answer.save()
        try:
            result_dic = fn(*args, **kwargs)

            answer.status = 'finished'
            answer.runtime = result_dic['judger']['result']
            answer.raw_result = result_dic['result']
            answer.cpu = result_dic['judger']['cpu_time']
            answer.memory = result_dic['judger']['memory']
            if result_dic['pass'] == True:
                answer.result = 0
                # for problem statistics
                p.pass_num += 1
                p.save()

                # update aggregation tables
                uaggr, created = OJUserAnswerAggr.objects.get_or_create(problem=p, submitter=owner)
                if created:
                    uaggr.answer = answer
                    uaggr.save()
                else:
                    oriAnswer = uaggr.answer
                    if answer.cpu < oriAnswer.cpu:
                        uaggr.answer = answer
                        uaggr.save()
                    elif answer.cpu == oriAnswer.cpu and answer.memory < oriAnswer.memory:
                        uaggr.answer = answer
                        uaggr.save()
                    else:
                        pass
            else:
                answer.result = 1

        except Exception as e:
            answer.status = 'failed'
            answer.raw_result = str(e)
        answer.save()
    
    return wrapper


@shared_task
@update_answer
def judge(source_code, input2, output2):
    from .submittasks import judgeOne

    taskObj = judgeOne.delay(input2, output2+'\n', source_code)
    with allow_join_result():
        result = taskObj.get(10)
    return result