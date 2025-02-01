import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
from init import AudioProcessor

def record_test_audio(duration=5, sample_rate=16000):
    """Record audio for testing"""
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1
    )
    sd.wait()  # Wait until recording is finished
    return recording

def save_audio(recording, filename="test_recording.wav", sample_rate=16000):
    """Save the recorded audio"""
    sf.write(filename, recording, sample_rate)
    return filename

def test_audio_conversion():
    # Create test directory if it doesn't exist
    test_dir = Path("test_audio")
    test_dir.mkdir(exist_ok=True)
    
    # Option 1: Record live audio
    print("Option 1: Record live audio")
    recording = record_test_audio()
    test_file = test_dir / "test_recording.wav"
    save_audio(recording, str(test_file))
    
    # Option 2: Create a test tone
    print("\nOption 2: Generate test tone")
    duration = 3  # seconds
    sample_rate = 16000
    t = np.linspace(0, duration, int(sample_rate * duration))
    test_tone = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
    test_tone_file = test_dir / "test_tone.wav"
    sf.write(str(test_tone_file), test_tone, sample_rate)
    
    # Process both audio files
    processor = AudioProcessor()
    
    print("\nProcessing recorded audio:")
    result1 = processor.process_call(str(test_file))
    print(f"Success: {result1['success']}")
    print(f"Transcribed text: {result1['text']}")
    
    print("\nProcessing test tone:")
    result2 = processor.process_call(str(test_tone_file))
    print(f"Success: {result2['success']}")
    print(f"Transcribed text: {result2['text']}")

if __name__ == "__main__":
    test_audio_conversion()