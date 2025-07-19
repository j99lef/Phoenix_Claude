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

echo "Starting gunicorn on port $PORT"
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --log-level debug --access-logfile - --error-logfile - --preload