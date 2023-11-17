.PHONY: quality style test

check_dirs := tests src benchmarks metrics utils

# Check that source code meets quality standards

quality:
	ruff check $(check_dirs)  # linter
	ruff format --check $(check_dirs) # formatter

# Format source code automatically

style:
	ruff check --fix $(check_dirs) # linter
	ruff format $(check_dirs) # formatter

# Run tests for the library

test:
	python -m pytest -n auto --dist=loadfile -s -v ./tests/
