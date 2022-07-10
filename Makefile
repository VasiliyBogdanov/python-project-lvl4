run-server:
	poetry run python3 manage.py runserver
make-migrations:
	poetry run python3 manage.py makemigrations
migrate:
	poetry run python3 manage.py migrate
generate-requirements:
	poetry export --without-hashes -f requirements.txt -o requirements.txt
make-messages:
	poetry run python3 manage.py makemessages --ignore="static" --ignore=".venv" -l ru
compile-messages:
	poetry run python3 manage.py compilemessages
test:
	poetry run python3 manage.py test 
lint:
	poetry run flake8 task_manager
test-coverage: 
	poetry run coverage run manage.py test
	poetry run coverage xml
.PHONY: run-server make-migrations migrate generate-requirements make-messages compile-messages test lint