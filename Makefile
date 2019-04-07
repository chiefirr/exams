install:
		virtualenv -p python3 ./venv
		( \
		source venv/bin/activate; \
		pip install -r requirements.txt; \
		)
		python manage.py migrate
		python manage.py loaddata exams_api/fixtures/base_auth.json
		python manage.py runserver 8000

test:
		pytest

serve:
		python manage.py runserver