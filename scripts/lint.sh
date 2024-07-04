#!/bin/bash
echo "Activating local environment"
source .venv/bin/activate

echo "Running pyup_dirs..."
pyup_dirs --py312-plus --recursive cashback_memory tests

echo "Running ruff..."
ruff cashback_memory tests --fix
