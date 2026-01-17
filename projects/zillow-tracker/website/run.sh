#!/bin/bash

echo "Starting Zillow Property Tracker Web Interface..."
echo "========================================"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    pip3 install Flask
fi

# Start the Flask application
echo "Starting server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 app.py
