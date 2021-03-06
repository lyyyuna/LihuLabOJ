import _judger
import os
import uuid
import grp
import pwd
from celery import Celery


rabbituser = os.environ.get('RABBIT_USER')
rabbitpass = os.environ.get('RABBIT_PASS')
rabbithost = os.environ.get('RABBIT_HOST')
rabbitport = os.environ.get('RABBIT_PORT')
rabbitvhost = os.environ.get('RABBIT_VHOST')
uri = 'amqp://{}:{}@{}:{}/{}'.format(rabbituser, rabbitpass, rabbithost, rabbitport, rabbitvhost)
app = Celery('tasks', broker=uri, backend='rpc://')

app.conf.update(
    worker_max_tasks_per_child = 20,
)


myuid = pwd.getpwnam('myuser').pw_uid
mygid = grp.getgrnam('myuser').gr_gid


@app.task
def judgeOne(realInput, expectedOutput, script):
    a = uuid.uuid1()
    answerId = str(a)
    inputFile = 'tmp/' + answerId + '.in'
    outputFile = 'tmp/' + answerId + '.out'
    scriptFile = 'tmp/' + answerId + '.py'
    with open(inputFile, 'w') as f:
        f.write(realInput)
    with open(scriptFile, 'w') as f:
        f.write(script)

    ret = _judger.run(max_cpu_time=1000,
                    max_real_time=2000,
                    max_memory=128 * 1024 * 1024,
                    max_process_number=20,
                    max_output_size=2048,
                    max_stack=32 * 1024 * 1024,
                    exe_path="/usr/bin/python3",
                    input_path=inputFile,
                    output_path=outputFile,
                    error_path=outputFile,
                    args=[scriptFile,],
                    env=[],
                    log_path="judger.log",
                    seccomp_rule_name="general",
                    uid=myuid,
                    gid=mygid)

    retDic = {}
    retDic['judger'] = ret
    with open(outputFile, 'r') as f:
        result = f.read()
        retDic['result'] = result
        if result == expectedOutput:
            retDic['pass'] = True
        else:
            retDic['pass'] = False
    os.remove(inputFile)
    os.remove(outputFile)
    os.remove(scriptFile)
    return retDic
