#!/bin/bash
echo "Starting TravelAiGent..."
echo "PORT environment variable: $PORT"

if [ -z "$PORT" ]; then
    echo "WARNING: PORT not set, using 5000"
    export PORT=5000
fi

echo "Starting gunicorn on port $PORT"
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --log-level info --access-logfile - --error-logfile -