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
test:
# Add app name you wish to test
	poetry run python3 manage.py test 
.PHONY: run-server make-migrations migrate generate-requirements make-messages compile-messages test