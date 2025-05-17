# Groq Whisperer

A voice-to-text application using Groq's Whisper model for fast, accurate transcription, with system-wide hotkey support and sound notifications.

## Features

- Real-time audio transcription using Groq's Whisper API
- System-wide hotkey support for starting/stopping recording
- Sound notifications for recording start/stop and completion
- Automatic text insertion at cursor position
- Australian/British English optimisation
- Intelligent handling of programming terminology and syntax
- Configurable audio device selection
- Environment-based configuration
- Background sound processing for minimal latency

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/groq_whisperer.git
cd groq_whisperer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Groq API key:
```bash
echo "GROQ_API_KEY=your-api-key-here" > .env
```

## System Integration

The application provides two scripts for system-wide integration:
- `run_recorder.sh`: Starts the recording service
- `stop_recorder.sh`: Stops the recording service

You can bind these to system-wide hotkeys. For example, create these scripts in your home directory:

```bash
# ~/meta-a.sh (Start recording)
#!/bin/bash
echo "meta-a ran at $(date)" >> "$HOME/shortcut_log.txt"
"$HOME/repos/groq_whisperer/run_recorder.sh"

# ~/meta-z.sh (Stop recording)
#!/bin/bash
echo "meta-z ran at $(date)" >> "$HOME/shortcut_log.txt"
"$HOME/repos/groq_whisperer/stop_recorder.sh"
```

Then bind your preferred hotkeys to these scripts using your desktop environment's settings.

## Configuration

The `.env` file supports the following settings:
```
GROQ_API_KEY=your_groq_api_key_here
AUDIO_DEVICE_INDEX=12  # Optional: Set to your preferred audio input device
```

## Audio Device Selection

If no `AUDIO_DEVICE_INDEX` is specified in `.env`, the application will:
1. List all available audio devices on startup
2. Attempt to find a suitable microphone automatically
3. Use the first available input device if no microphone is found

To set a specific device:
1. Run the application once to see the device list
2. Note your preferred device's index
3. Add `AUDIO_DEVICE_INDEX=<number>` to your `.env` file

## Sound Notifications

The application uses sound notifications to indicate:
- Recording start (single tone)
- Recording stop (double tone)
- Transcription complete (completion tone)

Sound files are located in the `sounds` directory:
- `start.mp3`: Used for recording start/stop
- `complete.mp3`: Used for transcription completion

## Dependencies

Key dependencies include:
- groq: For API access
- PyAudio: For audio recording
- pygame: For sound notifications
- python-dotenv: For environment configuration
- xdotool: For text insertion (system requirement)

## Troubleshooting

### Audio Issues
- Ensure your microphone is properly connected and selected
- Check the system sound settings
- Try specifying a different `AUDIO_DEVICE_INDEX` in `.env`

### Text Insertion Issues
- Ensure xdotool is installed on your system
- Check that your cursor is focused where you want the text

### Sound Notification Issues
- Ensure your system's sound is working
- Check that the MP3 files exist in the `sounds` directory
- Verify pygame is properly installed

## Credits

This project is a fork of [groq-whisperer](https://github.com/KennyVaneetvelde/groq_whisperer) by Kenny Vaneetvelde.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues and enhancement requests!
