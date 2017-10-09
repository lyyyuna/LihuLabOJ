#!/bin/sh

sleep 10

cd lihulaboj

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000