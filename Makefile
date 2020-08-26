.PHONY: quality style test test-examples

# Check that source code meets quality standards

quality:
	black --check --line-length 119 --target-version py36 tests src benchmarks
	isort --check-only --recursive tests src benchmarks datasets
	flake8 tests src benchmarks

# Format source code automatically

style:
	black --line-length 119 --target-version py36 tests src benchmarks
	isort --recursive tests src datasets benchmarks
