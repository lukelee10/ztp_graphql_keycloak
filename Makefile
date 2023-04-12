start: services-start ztpvis-start

setup:
	pip install pipenv
	PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --python $$(which python)

ztpvis-start:
	pipenv run uvicorn ztpvis.main:app --host 0.0.0.0 --port 8000 --reload

up: services-start
services-start:
	docker-compose -f docker-compose/docker-compose.yml up -d

stop: services-stop
services-stop:
	docker-compose -f docker-compose/docker-compose.yml stop

down: services-down
services-down:
	docker-compose -f docker-compose/docker-compose.yml down

logs:
	docker-compose -f docker-compose/docker-compose.yml logs -f