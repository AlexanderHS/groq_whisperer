#!/bin/bash

# Script to install Groq Whisperer

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Copy start script to home directory
log "Installing Groq Whisperer..."
cp "$SCRIPT_DIR/start_whisper.sh" ~/start_whispering.sh
chmod +x ~/start_whispering.sh

# Add alias to shell rc file
RC_FILE=~/.bashrc
if [ -f ~/.zshrc ]; then
    RC_FILE=~/.zshrc
fi

# Remove any existing Groq Whisperer aliases
if grep -q "# Groq Whisperer" "$RC_FILE"; then
    log "Removing old Groq Whisperer configuration..."
    sed -i '/# Groq Whisperer/,+1d' "$RC_FILE"
fi

# Add new alias at the end of the file
echo -e "\n# Groq Whisperer" >> "$RC_FILE"
echo 'alias groqw="~/start_whispering.sh"' >> "$RC_FILE"
log "Added 'groqw' alias to $RC_FILE"

log "Installation complete!"
log "NOTE: Your .bashrc has a syntax error. Please fix it before sourcing."
log "You can run Groq Whisperer by:"
log "1. Running directly: ~/start_whispering.sh"
log "2. After fixing .bashrc and sourcing it, using: groqw" 