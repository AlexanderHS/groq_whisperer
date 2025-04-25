#!/bin/bash

# Script to uninstall Groq Whisperer desktop application

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Stop and disable the service if it's running
log "Stopping service if running..."
systemctl --user stop groq-whisperer 2>/dev/null
systemctl --user disable groq-whisperer 2>/dev/null

# Remove service file
log "Removing service file..."
rm -f ~/.config/systemd/user/groq-whisperer.service

# Reload systemd to recognize the removal
log "Reloading systemd..."
systemctl --user daemon-reload

# Remove desktop entry
log "Removing desktop entry..."
rm -f ~/.local/share/applications/groq-whisperer.desktop

# Remove from autostart
log "Removing from autostart..."
rm -f ~/.config/autostart/groq-whisperer.desktop

# Clean up logs
log "Cleaning up logs..."
rm -rf ~/.local/share/groq-whisperer

# Update application database
log "Updating application database..."
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database ~/.local/share/applications
fi

log "Uninstallation complete!"
log "Note: The application files remain in their original location."
log "To completely remove, delete the application directory as well." 