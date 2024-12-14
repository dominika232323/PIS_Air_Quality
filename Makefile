# Variables
COV_FAIL=--cov-fail-under=80

# Targets
.PHONY: requirements migrations tests coverage clean start_db run stop_db up down

#Install requirements
requirements:
	pip install -r requirements.txt

#Make migrations
migrations:
	python3 ./Air_Quality/manage.py migrate

#Run all tests
tests:
	pytest ./Air_Quality

#Run tests with coverage
coverage:
	pytest ./Air_Quality --cov=. --cov-report=html $(COV_FAIL)

#Clean up coverage artifacts
clean:
	rm -rf htmlcov .coverage

#Start database
start_db:
	docker compose -f ./database/docker-compose.yml up -d

#Run Django server on http://localhost:8000/
run:
	python3 ./Air_Quality/manage.py runserver

#Stop database
stop_db:
	docker compose -f ./database/docker-compose.yml down

#Run application with one command:
up: migrations start_db run

#Make migrations
migrations-venv:
	./venv/bin/python3.12 ./PIS-proj/Air_Quality/manage.py migrate

#Start database
start_db-venv:
	docker compose -f ./PIS-proj/database/docker-compose.yml up -d

#Run Django server on http://localhost:8000/
run-venv:
	./venv/bin/python3.12 ./PIS-proj/Air_Quality/manage.py runserver


#Run application with one command:
up-venv: migrations-venv start_db-venv run-venv

#Stop application:
down: stop_db