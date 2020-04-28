.PHONY: quality style test test-examples

# Check that source code meets quality standards

quality:
	black --check --line-length 119 --target-version py36 src
	isort --check-only --recursive src
	flake8 src

# Format source code automatically

style:
	black --line-length 119 --target-version py36 src
	isort --recursive src
