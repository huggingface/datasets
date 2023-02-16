.PHONY: quality style test

check_dirs := tests src benchmarks metrics

# Check that source code meets quality standards

quality:
	black --check $(check_dirs)
	ruff $(check_dirs)

# Format source code automatically

style:
	black tests src benchmarks metrics
	ruff $(check_dirs) --fix

# Run tests for the library

test:
	python -m pytest -n auto --dist=loadfile -s -v ./tests/
