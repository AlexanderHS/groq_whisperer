# Groq Whisperer

A Python application that transcribes speech to text in real-time using Groq's Whisper implementation. This is a fork of [Kenny Vaneetvelde's work](https://github.com/kennyvv/groq-whisperer), enhanced with additional features and improvements.

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

## Prerequisites

- Python 3.x
- A Groq API key
- PyAudio compatible audio input device (e.g., microphone)
- Linux environment (tested on Linux 6.13.7-zen1-1-zen)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AlexanderHS/groq_whisperer.git
   cd groq_whisperer
   ```

2. Copy the environment template and configure your settings:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` and add your Groq API key and preferred audio device index.

3. Run the start script:
   ```bash
   ./start_whisper.sh
   ```

The script will automatically:
- Create a virtual environment if needed
- Install all required dependencies
- Configure your environment
- Start the application

## Usage

1. Run the application using `./start_whisper.sh`
2. The application will list available audio input devices
3. Press and hold the PAUSE key to record
4. Release the PAUSE key to stop recording
5. The transcription will be automatically copied to your clipboard

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

This project is a fork of [groq-whisperer](https://github.com/kennyvv/groq-whisperer) by Kenny Vaneetvelde.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues and enhancement requests!
