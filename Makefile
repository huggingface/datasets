.PHONY: quality style test

check_dirs := tests src benchmarks metrics utils

# Check that source code meets quality standards

quality:
	black --check $(check_dirs) setup.py
	ruff $(check_dirs) setup.py

# Format source code automatically

style:
	black tests src benchmarks metrics setup.py
	ruff $(check_dirs) setup.py --fix

# Run tests for the library

test:
	python -m pytest -n auto --dist=loadfile -s -v ./tests/
