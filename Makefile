.PHONY: quality style test test-examples

# Check that source code meets quality standards

quality:
	black --check --line-length 119 --target-version py36 src tests
	isort --check-only --recursive src tests
	flake8 src tests

# Format source code automatically

style:
	black --line-length 119 --target-version py36 src tests
	isort --recursive src tests
