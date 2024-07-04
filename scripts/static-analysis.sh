#!/bin/bash
echo "Activating local environment"
source .venv/bin/activate
set -e

echo "Running mypy..."
mypy cashback_memory

echo "Running bandit..."
bandit -c pyproject.toml -r cashback_memory
