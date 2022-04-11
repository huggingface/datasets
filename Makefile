.PHONY: quality style test

# Check that source code meets quality standards

quality:
	black --check --line-length 119 --target-version py36 tests src benchmarks datasets/**/*.py metrics
	isort --check-only tests src benchmarks datasets/**/*.py metrics
	flake8 tests src benchmarks datasets/**/*.py metrics

# Format source code automatically

style:
	black --line-length 119 --target-version py36 tests src benchmarks datasets/**/*.py metrics
	isort tests src benchmarks datasets/**/*.py metrics

# Run tests for the library

test:
	python -m pytest -n auto --dist=loadfile -s -v ./tests/
