#!/bin/bash
echo "Activating local environment"
source .venv/bin/activate

pytest tests
