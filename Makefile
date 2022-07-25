.PHONY: quality style test

# Check that source code meets quality standards

quality:
	black --check --line-length 119 --target-version py36 tests src benchmarks datasets/**/*.py
	isort --check-only tests src benchmarks datasets/**/*.py
	flake8 tests src benchmarks datasets/**/*.py

# Format source code automatically

style:
	black --line-length 119 --target-version py36 tests src benchmarks datasets/**/*.py
	isort tests src benchmarks datasets/**/*.py

# Run tests for the library

test:
	python -m pytest -n auto --dist=loadfile -s -v ./tests/
