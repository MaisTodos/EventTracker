test:
	poetry run pytest -svv --showlocals

isort:
	poetry run isort .

black:
	poetry run black .
