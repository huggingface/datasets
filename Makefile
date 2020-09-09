.PHONY: quality style test test-examples

# Check that source code meets quality standards

quality:
	black --check --line-length 119 --target-version py36 tests src benchmarks datasets metrics
	isort --check-only tests src benchmarks datasets metrics
	flake8 tests src benchmarks datasets metrics

# Format source code automatically

style:
	black --line-length 119 --target-version py36 tests src benchmarks datasets metrics
	isort tests src benchmarks datasets metrics
