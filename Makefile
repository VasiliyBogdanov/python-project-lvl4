install:
	poetry install
build:
	poetry build
package-install:
	python -m pip install --user --force-reinstall dist/*.whl
test:
	poetry run pytest -vv
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml
lint:
	poetry run flake8 page_loader
run-server:
	poetry run python3 manage.py runserver
make-migrations:
	poetry run python3 manage.py makemigrations
migrate:
	poetry run python3 manage.py migrate
generate-requirements:
	poetry export -f requirements.txt -o requirements.txt
.PHONY: install build package-install test test-coverage lint run-server make-migrations migrate