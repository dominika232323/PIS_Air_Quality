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
up: requirements migrations start_db run

#Stop application:
down: stop_db