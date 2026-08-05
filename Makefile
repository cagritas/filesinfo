.PHONY: install test lint format clean

install:
	pip install -e .[dev]

test:
	python3 -m unittest

lint:
	ruff check .
	black --check .

format:
	ruff check --fix .
	black .

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .ruff_cache/ __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
