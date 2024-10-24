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
	@pip install -r requirements.txt

install-test-dependencies:
	@echo "Installing dependencies..."
	@pip install -r requirements-test.txt

pull-hadolint:
	@echo "Pulling hadolint image..."
	@docker pull hadolint/hadolint

setup: venv install-dependencies install-test-dependencies pull-hadolint

#
# Lint: lint application code
#
hadolint-docker:
	@echo "Linting Dockerfile..."
	@docker run --rm -i hadolint/hadolint < Dockerfile

mypy:
	@echo "Running mypy..."
	@mypy action

black:
	@echo "Running black..."
	@black --check action

flake8:
	@echo "Running flake8..."
	@flake8 action

lint: hadolint-docker mypy black flake8

#
# Format: format action code
#

black-format:
	@echo "Running black..."
	@black action

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
	python main.py --github_repository package-maintenance-dev/github-action-maven-example

run-docker-action-maven-example:
	docker run pmd-github-action --github_repository package-maintenance-dev/github-action-maven-example

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