#!/bin/bash
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py loaddata exams_api/fixtures/base_auth.json
python manage.py loaddata exams_api/fixtures/base_exams.json
python manage.py runserver 0.0.0.0:8990