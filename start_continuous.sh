#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Install system dependencies if not present
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking system dependencies..."
for pkg in "portaudio" "python-pyaudio" "gcc" "pkg-config"; do
    if ! pacman -Qi "$pkg" > /dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Installing $pkg..."
        sudo pacman -S --noconfirm "$pkg" || echo "Warning: Could not install $pkg (might not be available in repos)"
    fi
done

# Check if virtual environment exists, create if it doesn't
if [ ! -d "venv" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Ensure all required packages are in requirements.txt
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Updating requirements..."
for package in "pyaudio" "simpleaudio" "pyautogui" "pyperclip" "groq" "python-dotenv"; do
    if ! grep -q "^$package" requirements.txt 2>/dev/null; then
        echo "$package" >> requirements.txt
    fi
done

# Install required packages
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Installing required packages..."
CFLAGS="-I/usr/include" LDFLAGS="-L/usr/lib" pip install -r requirements.txt

# Verify installations
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verifying installations..."
python -c "import pyaudio; import simpleaudio; import pyautogui; import pyperclip; import groq; from dotenv import load_dotenv" || {
    echo "Error: Some required packages failed to install properly."
    exit 1
}

# Ensure user is in the audio group
if ! groups | grep -q "audio"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Adding user to audio group..."
    sudo usermod -a -G audio $USER
    echo "Please log out and log back in for group changes to take effect."
    exit 1
fi

# Create sounds directory if it doesn't exist
mkdir -p sounds

# Create sound files if they don't exist (you'll need to provide the actual sound files)
if [ ! -f sounds/start.wav ] || [ ! -f sounds/complete.wav ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Please ensure sound files exist in the sounds directory:"
    echo "- sounds/start.wav"
    echo "- sounds/complete.wav"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Installation complete!"
echo "You can now use run_recorder.sh to start/stop recording." 