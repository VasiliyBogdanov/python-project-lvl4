### Hexlet tests and linter status:
[![Actions Status](https://github.com/VasiliyBogdanov/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/VasiliyBogdanov/python-project-lvl4/actions)
[![Python CI](https://github.com/VasiliyBogdanov/python-project-lvl4/actions/workflows/tests.yml/badge.svg)](https://github.com/VasiliyBogdanov/python-project-lvl4/actions/workflows/tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/b0a1d09c6db4694078ae/maintainability)](https://codeclimate.com/github/VasiliyBogdanov/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b0a1d09c6db4694078ae/test_coverage)](https://codeclimate.com/github/VasiliyBogdanov/python-project-lvl4/test_coverage)


### Description:
This is 4th and final project in Hexlet's 'Python developer' course,
Task Manager application made with Django.
This project includes: 
- user registration, authentication, restricting access
- implementation of 'tasks', 'labels' and 'statuses'
- task search with filtering (using 'django_filter' library)
- tests using Django test client
- deployment on Heroku, using PostgreSQL
- connecting Rollbar error tracking service <br/>
https://rollbar.com/

### App on Heroku:
https://python-task-manager-vb.herokuapp.com/

### Local installation:
1. Clone this project
2. Create .env file in root directory. Add two variables there:
```
SECRET_KEY='Your Django SECRET_KEY here'
```
```
ACCESS_TOKEN='token from Rollbar error tracker'
```

3. If you don't have poetry dependency manager, install it:
```
pip install poetry
```
4. Install dependencies:
```
poetry install
```
5. Make migrations and migrate:
```
poetry run python3 manage.py makemigrations
```
```
poetry run python3 manage.py migrate
```
   - If you have 'make' utility installed: <br/>
       ```
       make make-migrations
       ```
       ```
       make migrate
       ```
   - Also, there are other useful 'make' commands in Makefile, check it out 🧐
6. Launch server:
```
poetry run python3 manage.py runserver
```
or
```
make run-server
```