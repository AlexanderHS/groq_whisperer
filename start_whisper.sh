#!/bin/bash

# Script to start the Groq Whisperer application

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Log file location
LOG_DIR="$HOME/.local/share/groq-whisperer"
LOG_FILE="$LOG_DIR/whisperer.log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    log "Error: .env file not found!"
    log "Please copy .env.template to .env and fill in your API key."
    exit 1
fi

# Virtual environment path
VENV_PATH="$SCRIPT_DIR/venv"

# Check if virtual environment exists, if not create it
if [ ! -d "$VENV_PATH" ]; then
    log "Creating virtual environment..."
    python -m venv "$VENV_PATH"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Upgrade pip first
log "Upgrading pip..."
pip install --upgrade pip >/dev/null 2>&1

# Install required packages
log "Installing required packages..."
if ! pip install -r "$SCRIPT_DIR/requirements.txt" >/dev/null 2>&1; then
    log "Error: Failed to install required packages!"
    deactivate
    exit 1
fi

# Verify critical packages are installed
log "Verifying installations..."
if ! python -c "import groq, dotenv, pyaudio, keyboard" 2>/dev/null; then
    log "Error: Critical packages are missing!"
    deactivate
    exit 1
fi

# Run the application with proper permissions
log "Starting Groq Whisperer..."

# If running as a service, redirect output to log file
if [ "${1:-}" = "--service" ]; then
    exec sudo -E env PATH="$PATH" python "$SCRIPT_DIR/main.py" >> "$LOG_FILE" 2>&1
else
    # Interactive mode with output to terminal
    sudo -E env PATH="$PATH" python "$SCRIPT_DIR/main.py"
fi

# Deactivate virtual environment when done
deactivate