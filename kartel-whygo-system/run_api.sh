#!/bin/bash
# Start the FastAPI development server

cd "$(dirname "$0")"

echo "Starting Kartel WhyGO Management API..."
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""

# Run uvicorn with auto-reload
python3 -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
