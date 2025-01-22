# Variables
COV_FAIL=--cov-fail-under=80

# Targets
.PHONY: requirements migrations tests coverage clean start_db build_db run stop_db clean_db up down

#Install requirements
requirements:
	pip install -r requirements.txt

#Make migrations
migrations:
	sleep 3
	python3 ./Air_Quality/manage.py makemigrations && python3 ./Air_Quality/manage.py migrate

#Virtualenv Make migrations
migrations-venv:
	sleep 3
	../venv/bin/python3 ./Air_Quality/manage.py makemigrations  && ../venv/bin/python3 ./Air_Quality/manage.py migrate

#Run all tests
tests_withDB:
	pytest ./Air_Quality/gios_api/tests

DB_tests: start_db migrations tests_withDB

#Run tests not requiring db
tests:
	pytest ./Air_Quality/gios_api/tests/test_services.py

#Run tests with coverage
coverage:
	pytest ./Air_Quality/gios_api/tests --cov=. --cov-report=html $(COV_FAIL)

#Clean up coverage artifacts
clean:
	rm -rf htmlcov .coverage

#Start database
start_db:
	docker compose -f ./database/docker-compose.yml up -d

#Build database from ./database/build.sql
build_db:
	docker cp ./database/build.sql air-quality-db:/
	docker exec -it air-quality-db psql -U myuser -d airqualitydb -f /build.sql

update_db:
	python3 ./Air_Quality/manage.py update_db

#Run Django server on http://localhost:8000/
run:
	python3 ./Air_Quality/manage.py runserver &

#Stop database
stop_db:
	docker compose -f ./database/docker-compose.yml down -v --remove-orphans

#Clean database
clean_db:
	docker volume rm database_pgdata_volume

stop_server:
	pkill -f runserver

#Run Streamlit app
run_streamlit:
	streamlit run ./Air_Quality/app/app.py

runstreamlit-az:
	nohup ../venv/bin/python3 -m streamlit run ./Air_Quality/app/app.py --server.address 0.0.0.0 --server.port 8501 &

stop_streamlit:
	pkill -f streamlit

#Run application with one command:
up: requirements start_db migrations update_db run

#Run application with one command on az vm:
up-az: start_db migrations-venv run-az runstreamlit-az

#Vitrualenv Run Django server on az vm
run-az:
	nohup ../venv/bin/python3 ./Air_Quality/manage.py runserver 0:8000 &

#Stop application:
down: stop_db stop_server stop_streamlit