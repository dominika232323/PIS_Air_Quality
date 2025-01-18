# Variables
COV_FAIL=--cov-fail-under=80

# Targets
.PHONY: requirements migrations tests coverage clean start_db build_db run stop_db clean_db up down

#Install requirements
requirements:
	pip install -r requirements.txt

#Make migrations
migrations:
	python3 ./Air_Quality/manage.py makemigrations && python3 ./Air_Quality/manage.py migrate

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

#Build database from ./database/build.sql
build_db:
	docker cp ./database/build.sql air-quality-db:/
	docker exec -it air-quality-db psql -U myuser -d airqualitydb -f /build.sql

update_db:
	python3 ./Air_Quality/gios_api/db_operations.py

#Run Django server on http://localhost:8000/
run:
	python3 ./Air_Quality/manage.py runserver &

#Stop database
stop_db:
	docker compose -f ./database/docker-compose.yml down

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
up: requirements start_db migrations run

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
up-az: migrations-venv start_db run-az runstreamlit-az

#Stop application:
down: stop_db stop_server stop_streamlit