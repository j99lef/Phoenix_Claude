#!/bin/bash
echo "Starting TravelAiGent..."
echo "PORT environment variable: $PORT"
echo "Current directory: $(pwd)"
echo "Python version: $(python --version 2>&1)"
echo "Contents of current directory:"
ls -la

if [ -z "$PORT" ]; then
    echo "WARNING: PORT not set, using 5000"
    export PORT=5000
fi

echo "Running import tests..."
python test_import.py

echo "Starting TravelAiGent with scheduler on port $PORT"
# Run the combined web + scheduler process
exec python start_with_scheduler.py