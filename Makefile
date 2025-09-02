test:
	poetry run pytest -vs

isort:
	poetry run isort .

black:
	poetry run black .
