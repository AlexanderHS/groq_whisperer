#!/usr/bin/env python3
import numpy as np
import wave
import struct

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """Generate a sine wave with given frequency and duration"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave_data

def apply_envelope(wave_data, sample_rate, attack=0.1, decay=0.2):
    """Apply an ADSR envelope to the wave data"""
    samples = len(wave_data)
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    
    # Create envelope
    envelope = np.ones(samples)
    # Attack
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # Decay
    envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
    
    return wave_data * envelope

def save_wave_file(filename, wave_data, sample_rate=44100):
    """Save wave data to a WAV file"""
    # Normalize to 16-bit range
    normalized = np.int16(wave_data * 32767)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Convert to bytes and write
        for sample in normalized:
            wav_file.writeframes(struct.pack('h', sample))

def generate_start_sound():
    """Generate a pleasant start sound"""
    duration = 3.0
    sample_rate = 44100
    
    # Create a rising tone
    base_freq = 440  # A4 note
    wave1 = generate_sine_wave(base_freq, duration, sample_rate)
    wave2 = generate_sine_wave(base_freq * 1.5, duration, sample_rate)  # Perfect fifth
    
    # Combine waves
    combined = (wave1 + wave2) / 2
    
    # Apply envelope
    final_wave = apply_envelope(combined, sample_rate, attack=0.1, decay=0.3)
    
    # Save to file
    save_wave_file('sounds/start.wav', final_wave)

def generate_complete_sound():
    """Generate a pleasant completion sound"""
    duration = 3.0
    sample_rate = 44100
    
    # Create a descending tone
    base_freq = 880  # A5 note
    wave1 = generate_sine_wave(base_freq, duration, sample_rate)
    wave2 = generate_sine_wave(base_freq * 1.25, duration, sample_rate)  # Major third
    
    # Combine waves
    combined = (wave1 + wave2) / 2
    
    # Apply envelope
    final_wave = apply_envelope(combined, sample_rate, attack=0.1, decay=0.4)
    
    # Save to file
    save_wave_file('sounds/complete.wav', final_wave)

if __name__ == "__main__":
    print("Generating start sound...")
    generate_start_sound()
    print("Generating complete sound...")
    generate_complete_sound()
    print("Done! New sound files have been created in the sounds directory.") 