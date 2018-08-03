from __future__ import absolute_import, unicode_literals
from celery import shared_task
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
        profile = owner.ojuserprofile

        answer.status = 'started'
        answer.save()
        try:
            result_dic = fn(*args, **kwargs)

            answer.status = 'finished'
            answer.runtime = result_dic['judger']['result']
            answer.raw_result = result_dic['result']
            answer.cpu = result_dic['judger']['cpu_time']
            answer.memory = result_dic['judger']['memory']
            # update profile
            profile.total_num += 1
            # for problem statistics
            p.pass_num += 1
            if result_dic['pass'] == True:
                answer.result = 0
                # update aggregation tables
                uaggr, created = OJUserAnswerAggr.objects.get_or_create(problem=p, submitter=owner)
                if created:
                    uaggr.answer = answer
                    uaggr.cpu = answer.cpu
                    uaggr.memory = answer.memory
                    uaggr.save()
                    # update user profile
                    profile.pass_num += 1
                else:
                    if answer.cpu < uaggr.cpu:
                        uaggr.answer = answer
                        uaggr.cpu = answer.cpu
                        uaggr.memory = answer.memory
                        uaggr.save()
                    elif answer.cpu == uaggr.cpu and answer.memory < uaggr.memory:
                        uaggr.answer = answer
                        uaggr.cpu = answer.cpu
                        uaggr.memory = answer.memory
                        uaggr.save()
                    else:
                        pass
            else:
                answer.result = 1

        except Exception as e:
            answer.status = 'failed'
            answer.raw_result = str(e)
        answer.save()
        profile.save()
        p.save()
    
    return wrapper


@shared_task
@update_answer
def judge(source_code, input2, output2):
    from .submittasks import judgeOne

    res = judgeOne.delay(input2, output2+'\n', source_code)

    # wait at most 20 seconds
    # celery doesn't allow res.get(20) in another tasks, 
    # so I use this way instead
    cnt = 20
    while not res.ready() and cnt>0:
        time.sleep(1)
        cnt -= 1
    print cnt
    print res.result
    return res.result