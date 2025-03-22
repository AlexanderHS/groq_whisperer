import os
import tempfile
import wave
import pyaudio
import keyboard
import pyautogui
import pyperclip
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def list_audio_devices():
    """
    List all available audio input devices
    """
    p = pyaudio.PyAudio()
    info = []
    print("\nAvailable Audio Input Devices:")
    print("-" * 60)
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info.get('maxInputChannels') > 0:  # Only input devices
            print(f"Index {i}: {dev_info.get('name')}")
            info.append(dev_info)
    print("-" * 60)
    p.terminate()
    return info


def record_audio(sample_rate=48000, channels=2, chunk=1024, input_device_index=None):
    """
    Record audio from the microphone while the PAUSE button is held down.
    """
    p = pyaudio.PyAudio()
    
    # If no input device specified, try to find a default one
    if input_device_index is None:
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            if dev_info.get('maxInputChannels') > 0:
                input_device_index = i
                break
    
    # Get device info and print it for debugging
    try:
        device_info = p.get_device_info_by_index(input_device_index)
        print(f"\nDevice Info for index {input_device_index}:")
        print(f"Name: {device_info.get('name')}")
        print(f"Max Input Channels: {device_info.get('maxInputChannels')}")
        print(f"Default Sample Rate: {device_info.get('defaultSampleRate')}")
    except Exception as e:
        print(f"Error getting device info: {e}")
    
    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk,
        input_device_index=input_device_index,
        stream_callback=None
    )

    print("Press and hold the PAUSE button to start recording...")
    frames = []

    keyboard.wait("pause")  # Wait for PAUSE button to be pressed
    print("Recording... (Release PAUSE to stop)")

    while keyboard.is_pressed("pause"):
        try:
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
        except OSError as e:
            print(f"Warning: {str(e)}")
            continue

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames, sample_rate


def save_audio(frames, sample_rate):
    """
    Save recorded audio to a temporary WAV file.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        wf = wave.open(temp_audio.name, "wb")
        wf.setnchannels(2)  # Stereo
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
        return temp_audio.name


def transcribe_audio(audio_file_path):
    """
    Transcribe audio using Groq's Whisper implementation.
    """
    try:
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model="whisper-large-v3-turbo",  # Using turbo model for potentially faster responses
                prompt="""Australian software developer using British/Australian spelling (colour, optimise, centre).
                Context: Python programming, technical discussions.
                Expected content:
                - Programming terms (Python, Git, Docker)
                - Code syntax and commands
                - File paths (/home/user/, .py, .env)
                - Technical jargon and package names
                Please transcribe symbols exactly ('underscore' for _, 'dot' for .) and maintain proper capitalisation of technical terms.""",
                response_format="text",
                language="en",
            )
        return transcription  # This is now directly the transcription text
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def copy_transcription_to_clipboard(text):
    """
    Copy the transcribed text to clipboard using pyperclip.
    """
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")


def main():
    # First list available devices
    list_audio_devices()
    
    # Use the configured microphone index from environment variables, or default to None
    AUDIO_DEVICE_INDEX = os.getenv("AUDIO_DEVICE_INDEX")
    if AUDIO_DEVICE_INDEX is not None:
        AUDIO_DEVICE_INDEX = int(AUDIO_DEVICE_INDEX)
    
    while True:
        # Record audio
        if AUDIO_DEVICE_INDEX is not None:
            print(f"\nUsing input device index {AUDIO_DEVICE_INDEX}")
        frames, sample_rate = record_audio(input_device_index=AUDIO_DEVICE_INDEX)

        # Add debug info about the recorded audio
        print(f"Recorded {len(frames)} frames at {sample_rate}Hz")
        if frames and len(frames) > 0:
            print(f"First frame size: {len(frames[0])} bytes")
        
        # Save audio to temporary file
        temp_audio_file = save_audio(frames, sample_rate)
        print(f"Saved audio to temporary file: {temp_audio_file}")

        # Transcribe audio
        print("Transcribing...")
        transcription = transcribe_audio(temp_audio_file)

        # Copy transcription to clipboard
        if transcription:
            print("\nTranscription:")
            print(transcription)
            print("Copying transcription to clipboard...")
            copy_transcription_to_clipboard(transcription)
            print("Transcription copied to clipboard and pasted into the application.")
        else:
            print("Transcription failed.")

        # Clean up temporary file
        os.unlink(temp_audio_file)

        print("\nReady for next recording. Press PAUSE to start.")


if __name__ == "__main__":
    main()
