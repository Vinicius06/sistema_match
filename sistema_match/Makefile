pytest:
	pytest
pycov:
	pytest --cov=usuarios tests/
	pytest --cov=usuarios --cov-report=html tests/

pylint:
	pylint --max-line-length=200 usuarios

run:
	python manage.py runserver

install:
	pip install -r requirements.txt