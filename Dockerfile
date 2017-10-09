FROM python:3.5

ADD requirements.txt /app/requirements

WORKDIR /app/

RUN pip install -r requirements.txt