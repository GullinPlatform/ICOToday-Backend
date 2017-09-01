#!/bin/bash

mkdir -p ../local

rm -rf *.pyc

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
