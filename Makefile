# Variables
VENV_DIR = venv
PYTHON = python3

# Default target
.PHONY: all
all: setup

#
# Setup: create a virtual environment, install dependencies etc.
#
.PHONY: venv
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)

install-dependencies:
	@echo "Installing dependencies..."
	@pip install .
	@pip install .[lint]
	@pip install .[test]

pull-hadolint:
	@echo "Pulling hadolint image..."
	@docker pull hadolint/hadolint

setup: venv install-dependencies pull-hadolint

#
# Clean: clean up build artifacts
#
clean:
	@echo "Cleaning up..."
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf .coverage
	@rm -rf .coverage.*
	@find . -name "*.log" -type f -delete

#
# Lint: lint application code
#
hadolint-docker:
	@echo "Linting Dockerfile..."
	@docker run --rm -i hadolint/hadolint < Dockerfile

mypy:
	@echo "Running mypy..."
	@mypy src

black:
	@echo "Running black..."
	@black --check src

flake8:
	@echo "Running flake8..."
	@flake8 src

lint: hadolint-docker mypy black flake8

#
# Format: format action code
#

black-format:
	@echo "Running black..."
	@black src

format: black-format

#
# Build: build action docker image
#
build-action-docker:
	docker build -t pmd-github-action:latest .

build: build-action-docker

#
# Run examples: run action on example repositories
#
run-action-maven-example:
	@echo "Running action on Maven example repository..."
	@mkdir -p .local
	python main.py --github_repository package-maintenance-dev/github-action-maven-example > .local/maven-example-output.md

run-action-gradle-example:
	@echo "Running action on Gradle example repository..."
	@mkdir -p .local
	python main.py --github_repository package-maintenance-dev/github-action-gradle-example > .local/gradle-example-output.md

run-docker-action-maven-example:
	docker run -e GITHUB_REPOSITORY=package-maintenance-dev/github-action-maven-example pmd-github-action

run-docker-action-gradle-example:
	docker run -e GITHUB_REPOSITORY=package-maintenance-dev/github-action-gradle-example pmd-github-action

run-examples: run-action-maven-example

#
# Test: test action
#

pytest:
	@echo "Running pytest..."
	export PYTHONPATH=.
	@pytest tests -vv

test: pytest

#
# Continuous Integration workflow: setup, lint, build, test
# Should be run on any push to any branch.
#
ci: setup lint build test

#
# Pre-commit workflow: format, lint, build, test
# Should be run on locally before pushing changes to catch easy to fix bugs locally.
#
pre-commit: format lint build test