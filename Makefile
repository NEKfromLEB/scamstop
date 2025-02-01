# Variables
PYTHON = python3
PIP = pip3
VENV = venv
VENV_BIN = $(VENV)/bin

# Default target
.DEFAULT_GOAL := help

# Create virtual environment
$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install -r requirements.txt

# Install dependencies
.PHONY: install
install: $(VENV)/bin/activate

# Run tests
.PHONY: test
test: install
	$(VENV_BIN)/pytest tests/

# Clean up generated files and virtual environment
.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Format code
.PHONY: format
format: install
	$(VENV_BIN)/black .
	$(VENV_BIN)/isort .

# Run linting
.PHONY: lint
lint: install
	$(VENV_BIN)/flake8 .
	$(VENV_BIN)/mypy .

# Help command
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install  - Create virtual environment and install dependencies"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Remove virtual environment and cache files"
	@echo "  make format   - Format code using black and isort"
	@echo "  make lint     - Run linting checks"
	@echo "  make help     - Show this help message"
