# Groq Whisperer

A voice-to-text application using Groq's Whisper model for fast, accurate transcription.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/groq_whisperer.git
cd groq_whisperer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Groq API key:
```bash
echo "GROQ_API_KEY=your-api-key-here" > .env
```

4. Run the install script:
```bash
./install.sh
```

This will:
- Copy the start script to your home directory as `start_whispering.sh`
- Add a `groqw` alias to your shell configuration

## Usage

After installation, you can start the application in two ways:

1. Run directly:
```bash
~/start_whispering.sh
```

2. Use the alias (after sourcing your shell configuration):
```bash
source ~/.bashrc  # or ~/.zshrc
groqw
```

Once running:
- Hold the PAUSE key to record
- Release to stop recording and transcribe
- The transcription will be automatically copied to your clipboard

## Requirements

- Python 3.8+
- PyAudio
- A Groq API key
- A microphone

## Features

- Real-time audio transcription using Groq's Whisper API
- Hold-to-speak functionality using the PAUSE key
- Automatic clipboard integration
- Australian/British English optimisation
- Intelligent handling of programming terminology and syntax
- Configurable audio device selection
- Environment-based configuration

## Improvements Over Original

This fork includes several enhancements:
- Support for Australian/British English spelling conventions
- Enhanced Whisper prompting for better technical term recognition
- Proper environment variable management with `.env` support
- Improved audio device handling and configuration
- Better error handling and debugging output
- Comprehensive installation script with dependency management
- Structured project organization with `.gitignore` and requirements

## Configuration

The `.env` file supports the following settings:
```
GROQ_API_KEY=your_groq_api_key_here
AUDIO_DEVICE_INDEX=12  # Set to your preferred audio input device
```

## Troubleshooting

If you encounter audio device issues:
1. Run the application to see a list of available audio devices
2. Note the index of your preferred device
3. Update the `AUDIO_DEVICE_INDEX` in your `.env` file

## Dependencies

All required packages are listed in `requirements.txt` and are automatically installed by the start script. Key dependencies include:
- groq
- PyAudio
- keyboard
- PyAutoGUI
- python-dotenv

## Credits

This project is a fork of [groq-whisperer](https://github.com/KennyVaneetvelde/groq_whisperer) by Kenny Vaneetvelde.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues and enhancement requests!
