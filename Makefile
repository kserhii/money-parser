
all: test


.develop: requirements/dev.txt
	pip install -U -r requirements/dev.txt


test: .develop
	pytest ./tests ./money_parser --flake8


vtest: .develop
	pytest ./tests ./money_parser -v --flake8


cov: .develop
	pytest --cov money_parser --cov-report html --cov-report term ./tests/ ./money_parser/ --flake8
	@echo "open file://`pwd`/htmlcov/index.html"


clean:
	@find . \( \
		-name "__pycache__" -o \
		-name "*.pyc" -o \
		-name ".cache" -o \
		-name "*.egg-info" \) \
		-prune \
		-exec rm -rf {} \;
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf dist
	@rm -rf build
