test:
	poetry run pytest -vv
test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml
run-server:
	poetry run python3 manage.py runserver
make-migrations:
	poetry run python3 manage.py makemigrations
migrate:
	poetry run python3 manage.py migrate
generate-requirements:
	poetry export -f requirements.txt -o requirements.txt
make-messages:
	poetry run python3 manage.py makemessages --ignore="static" --ignore=".venv" -l ru
compile-messages:
	poetry run python3 manage.py compilemessages
.PHONY: install build package-install test test-coverage lint run-server make-migrations migrate