install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report=xml

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_analyzer
