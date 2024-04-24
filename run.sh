#!/bin/bash

# Check if virtual environment folder exists and activate it
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "msys" ]]; then
        # If on Windows (MSYS), use the appropriate activation script
        source venv/Scripts/activate
    else
        # For Linux/macOS, use the standard activation script
        source venv/bin/activate
    fi
else
    echo "Virtual environment folder 'venv' not found."
    exit 1
fi

# Check if .env file exists
if [ -f ".env" ]; then
    echo ".env file found."
else
    echo "Warning: .env file not found."
fi

# Run the Python application
python app.py
