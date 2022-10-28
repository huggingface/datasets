.PHONY: quality style test

# Check that source code meets quality standards

quality:
	black --check tests src benchmarks metrics
	isort --check-only tests src benchmarks metrics
	flake8 tests src benchmarks metrics

# Format source code automatically

style:
	black tests src benchmarks metrics
	isort tests src benchmarks metrics

# Run tests for the library

test:
	python -m pytest -n auto --dist=loadfile -s -v ./tests/
