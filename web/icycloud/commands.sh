#!/bin/bash
python manage.py runserver 0.0.0.0:8080
python manage.py celery worker --loglevel=info
