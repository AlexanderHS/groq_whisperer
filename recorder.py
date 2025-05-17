#!/usr/bin/env python3
import os
import tempfile
import wave
import pyaudio
import time
from groq import Groq
from dotenv import load_dotenv
import subprocess
import pygame  # Add pygame for MP3 playback
import threading

# Load environment variables
load_dotenv()

# Initialize pygame mixer for MP3 playback
pygame.mixer.init()

# Set up Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Lock file paths
LOCK_FILE = ".recorder.lock"
STOP_FILE = ".recorder.stop"

# Sound file paths
START_SOUND = "sounds/start.mp3"
COMPLETE_SOUND = "sounds/complete.mp3"

def check_lock():
    """Check if another instance is running"""
    if os.path.exists(LOCK_FILE):
        print("Another recording instance is already running.")
        print(f"If this is incorrect, delete the {LOCK_FILE} file and try again.")
        return True
    return False

def create_lock():
    """Create lock file"""
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def remove_lock():
    """Remove lock file"""
    try:
        os.remove(LOCK_FILE)
    except FileNotFoundError:
        pass

def check_stop_signal():
    """Check if stop file exists"""
    return os.path.exists(STOP_FILE)

def remove_stop_signal():
    """Remove stop file if it exists"""
    try:
        os.remove(STOP_FILE)
    except FileNotFoundError:
        pass

def list_audio_devices():
    """List all available audio input devices"""
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

def find_best_microphone():
    """Find the first device with 'Microphone' in the name"""
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info.get('maxInputChannels') > 0 and 'microphone' in dev_info.get('name', '').lower():
            p.terminate()
            return i
    p.terminate()
    return None

def play_sound_blocking(sound_file):
    """Play an MP3 file and wait for it to finish"""
    try:
        # Ensure mixer is initialized and not busy
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        # Stop any currently playing sounds
        pygame.mixer.music.stop()
        # Load and play
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        # Wait for it to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        # Small pause to ensure sound is fully played
        time.sleep(0.1)
    except Exception as e:
        print(f"Warning: Could not play sound {sound_file}: {e}")

def play_sound_nonblocking(sound_file):
    """Play an MP3 file in a background thread"""
    def _play():
        try:
            # Ensure mixer is initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Warning: Could not play sound {sound_file}: {e}")
    
    thread = threading.Thread(target=_play)
    thread.daemon = True  # Thread will exit when main program exits
    thread.start()

def play_double_start_nonblocking():
    """Play start sound twice in background"""
    def _play_double():
        try:
            # Ensure mixer is initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(START_SOUND)
            pygame.mixer.music.play()
            time.sleep(0.3)  # Small delay between plays
            # Ensure the second play works
            pygame.mixer.music.load(START_SOUND)  # Reload to ensure it plays
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Warning: Could not play double start sound: {e}")
    
    thread = threading.Thread(target=_play_double)
    thread.daemon = True
    thread.start()

def record_audio(duration=6000, sample_rate=48000, channels=2, chunk=1024, input_device_index=None):
    """Record audio for a fixed duration or until stop signal"""
    p = pyaudio.PyAudio()
    
    # If no input device specified, try to find a default one
    if input_device_index is None:
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            if dev_info.get('maxInputChannels') > 0:
                input_device_index = i
                break
    
    # Get device info
    try:
        device_info = p.get_device_info_by_index(input_device_index)
        print(f"\nUsing: {device_info.get('name')}")
    except Exception as e:
        print(f"Error getting device info: {e}")
    
    print(f"Recording... (Create {STOP_FILE} to stop)")
    
    # Ensure start sound plays and is heard
    print("Playing start sound...")
    play_sound_blocking(START_SOUND)
    print("Start sound complete, beginning recording...")
    
    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk,
        input_device_index=input_device_index
    )
    
    frames = []
    
    # Calculate total chunks needed for the duration
    total_chunks = int((sample_rate * duration) / chunk)
    start_time = time.time()
    last_update = 0
    last_check = 0
    
    try:
        for _ in range(total_chunks):
            current_time = time.time()
            
            # Check for stop signal every second
            if current_time - last_check >= 1:
                if check_stop_signal():
                    print("\nStop signal received.")
                    # Play double start sound in background
                    play_double_start_nonblocking()
                    break
                last_check = current_time
                
            try:
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)
            except OSError as e:
                print(f"Warning: {str(e)}")
                continue
            
            # Update progress every second
            elapsed = current_time - start_time
            current_second = int(elapsed)
            if current_second > last_update:
                mins, secs = divmod(current_second, 60)
                print(f"\rRecording: {mins:02d}:{secs:02d}", end="", flush=True)
                last_update = current_second
                
    finally:
        print("\nStopping...")
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    # Only process if we got some audio
    if frames:
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        print(f"Recorded {mins:02d}:{secs:02d}")
        return frames, sample_rate
    return None, None

def save_audio(frames, sample_rate):
    """Save recorded audio to a temporary WAV file"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        wf = wave.open(temp_audio.name, "wb")
        wf.setnchannels(2)  # Stereo
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
        return temp_audio.name

def transcribe_audio(audio_file_path):
    """Transcribe audio using Groq's Whisper implementation"""
    try:
        print("Transcribing...")
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model="whisper-large-v3-turbo",
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
            # Strip any leading/trailing whitespace from the transcription
            return transcription.strip() if transcription else None
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None

def type_text_at_cursor(text):
    """Type text at current cursor position using xdotool"""
    if not text:
        return
        
    try:
        # Use xdotool to type the text
        # We use --clearmodifiers to ensure no stuck modifier keys
        subprocess.run([
            'xdotool', 'type', '--clearmodifiers', '--delay', '1',
            text
        ], check=True)
        
        print("Text has been typed at cursor position.")
    except subprocess.CalledProcessError as e:
        print(f"Error typing text: {e}")
    except Exception as e:
        print(f"Unexpected error while typing text: {e}")

def append_transcription(text):
    """Handle transcribed text"""
    if text:
        # First type at cursor
        type_text_at_cursor(text)
        
        # Then append to log file (optional)
        output_file = os.path.expanduser("~/transcriptions.txt")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(output_file, "a") as f:
            f.write(f"\n[{timestamp}]\n{text}\n")
            f.write("-" * 80 + "\n")
        
        # Play completion sound in background
        play_sound_nonblocking(COMPLETE_SOUND)

def main():
    # Check if another instance is running
    if check_lock():
        return
        
    # Create lock file
    create_lock()
    
    try:
        # Remove any stale stop signal
        remove_stop_signal()
        
        # Try to get configured device
        AUDIO_DEVICE_INDEX = os.getenv("AUDIO_DEVICE_INDEX")
        selected_device = None
        
        if AUDIO_DEVICE_INDEX is not None:
            # Strip any comments and whitespace
            AUDIO_DEVICE_INDEX = AUDIO_DEVICE_INDEX.split('#')[0].strip()
            try:
                selected_device = int(AUDIO_DEVICE_INDEX)
            except ValueError:
                print(f"Warning: Invalid AUDIO_DEVICE_INDEX value '{AUDIO_DEVICE_INDEX}'")
        
        # If no valid config, try to find a microphone
        if selected_device is None:
            print("No valid device configured in .env")
            print("\nAvailable devices:")
            list_audio_devices()
            
            selected_device = find_best_microphone()
            if selected_device is not None:
                print(f"\nTip: Found a microphone at index {selected_device}")
                print("Add AUDIO_DEVICE_INDEX={selected_device} to .env to skip device listing")
            else:
                print("\nTip: Add AUDIO_DEVICE_INDEX=<number> to .env to select a device")
                return
        
        # Record audio
        frames, sample_rate = record_audio(duration=120, input_device_index=selected_device)
        
        if frames:
            # Save to temporary file
            temp_audio_file = save_audio(frames, sample_rate)
            
            try:
                # Transcribe
                transcription = transcribe_audio(temp_audio_file)
                
                # Append to file
                append_transcription(transcription)
                
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_audio_file)
                except Exception as e:
                    print(f"Warning: Could not delete temporary file: {e}")
        else:
            print("No audio recorded.")
            
    finally:
        # Always clean up lock file
        remove_lock()
        remove_stop_signal()

if __name__ == "__main__":
    main() 