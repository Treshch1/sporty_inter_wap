isort-check:
	isort --check --skip .env --resolve-all-configs .

black-check:
	black --check .

pylama:
	pylama

check: isort-check black-check pylama

run-tests:
	docker compose run --rm tests
