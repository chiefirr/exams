#!/bin/bash
set -e
python manage.py migrate
python manage.py loaddata exams_api/fixtures/base_auth.json
python manage.py loaddata exams_api/fixtures/base_exams.json
python manage.py collectstatic --no-input
