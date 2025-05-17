#!/bin/bash

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to clean up on exit
cleanup() {
    echo -e "\nStopping recorder..."
    touch .recorder.stop
    # Wait for recorder to finish and clean up
    while [ -f .recorder.lock ]; do
        sleep 0.5
    done
    # Remove stop file if it still exists
    rm -f .recorder.stop
    exit 0
}

# Set up trap for Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM

# Activate virtual environment
source venv/bin/activate

# Run the recorder with ALSA errors redirected to /dev/null
exec 2> >(grep -v -E "ALSA lib|Invalid card" >&2)
python recorder.py 