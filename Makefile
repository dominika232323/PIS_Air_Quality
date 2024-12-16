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
	python3 ./Air_Quality/manage.py runserver &

#Stop database
stop_db:
	docker compose -f ./database/docker-compose.yml down

stop_server:
	pkill -f runserver

#Run Streamlit app
run_streamlit:
	streamlit run ./Air_Quality/app/app.py

#Run application with one command:
up: requirements migrations start_db run run_streamlit

#Virtualenv Make migrations
migrations-venv:
	../venv/bin/python3 ./Air_Quality/manage.py migrate

#Vitrualenv Run Django server on http://localhost:8000/
run-venv:
	nohup ../venv/bin/python3 ./Air_Quality/manage.py runserver &

#Vitrualenv Run Django server on az vm
run-az:
	nohup ../venv/bin/python3 ./Air_Quality/manage.py runserver 0:8000 &

#Run application with one command in virtualenv:
up-venv: migrations-venv start_db run-venv

#Run application with one command on az vm:
up-az: migrations-venv start_db run-az

#Stop application:
down: stop_db stop_server