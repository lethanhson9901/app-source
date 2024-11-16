#!/bin/bash

echo "Checking Python version..."
poetry run python --version

echo "Checking if tools are installed..."
poetry run pip list | grep -E "bandit|safety"

echo "Testing bandit..."
poetry run bandit --version

echo "Testing safety..."
poetry run safety --version

echo "Creating test report..."
mkdir -p reports
poetry run bandit -r . --format json --output reports/test.json || true

if [ -f reports/test.json ]; then
    echo "Bandit scan successful!"
    echo "Output file created at reports/test.json"
else
    echo "Bandit scan failed!"
fi
