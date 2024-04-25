#!/bin/bash

# Check if .env file exists
if [ -f ".env" ]; then
    echo ".env file found."
else
    echo "Error: .env file not found. Exiting."
    exit 1  # Exit the script if .env file is not found
fi

# Run the Python application
python app.py
