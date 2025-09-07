test:
	poetry run pytest -svv --showlocals

coverage:
	poetry run coverage run -m pytest 
	poetry run coverage report -m
	poetry run coverage html

isort:
	poetry run isort .

black:
	poetry run black .
