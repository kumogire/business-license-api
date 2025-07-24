.PHONY: install dev test lint format clean migration upgrade downgrade

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

test:
	pytest tests/ -v --cov=app --cov-report=html

test-watch:
	pytest-watch tests/ -v

lint:
	ruff check app tests
	black --check app tests

format:
	black app tests
	ruff --fix app tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Database commands
init-db:
	python -m app.cli init-db

migration:
	python -m app.cli create-migration -m "$(msg)"

upgrade:
	python -m app.cli upgrade

downgrade:
	python -m app.cli downgrade

current:
	python -m app.cli current

history:
	python -m app.cli history

# Docker commands
docker-build:
	docker build -t business-license-api .

docker-run:
	docker run -p 8080:8080 --env-file .env business-license-api