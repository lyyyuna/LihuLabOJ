from celery import Celery
import os


rabbituser = os.environ.get('RABBIT_USER')
rabbitpass = os.environ.get('RABBIT_PASS')
rabbithost = os.environ.get('RABBIT_HOST')
rabbitport = os.environ.get('RABBIT_PORT')
rabbitvhost = os.environ.get('RABBIT_VHOST')
uri = 'amqp://{}:{}@{}:{}/{}'.format(rabbituser, rabbitpass, rabbithost, rabbitport, rabbitvhost)
app = Celery('tasks', broker=uri, backend='rpc://')


@app.task(name='tasks.judgeOne')
def judgeOne(realInput, expectedOutput, script):
    return 'pass'