install:
	poetry install


build:
	./build.sh


dev:
	poetry run flask --app page_analyzer:app run


make lint:
	poetry run flake8 page_analyzer


PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

test:
	poetry run pytest


test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml
