#!/bin/bash

# Script to start the Groq Whisperer application

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.template to .env and fill in your API key."
    exit 1
fi

# Virtual environment path
VENV_PATH="$SCRIPT_DIR/venv"

# Check if virtual environment exists, if not create it
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_PATH"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Upgrade pip first
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "Installing required packages..."
if ! pip install -r "$SCRIPT_DIR/requirements.txt"; then
    echo "Error: Failed to install required packages!"
    deactivate
    exit 1
fi

# Verify critical packages are installed
echo "Verifying installations..."
if ! python -c "import groq, dotenv, pyaudio, keyboard" 2>/dev/null; then
    echo "Error: Critical packages are missing!"
    deactivate
    exit 1
fi

# Run the application with proper permissions
echo "Starting Groq Whisperer..."
sudo -E env PATH="$PATH" python "$SCRIPT_DIR/main.py"

# Deactivate virtual environment when done
deactivate