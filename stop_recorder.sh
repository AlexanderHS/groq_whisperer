#!/bin/bash

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"


# Create the stop file to signal the recorder to stop
touch .recorder.stop

# Wait for the recorder to finish
while [ -f .recorder.lock ]; do
    echo "Waiting for recorder to finish..."
    sleep 1
done

echo "Recorder stopped." 