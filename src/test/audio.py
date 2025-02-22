import sys
from pathlib import Path
# Define BASE_DIR relative to this file
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent))

import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
from db.init import AudioProcessor

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

def test_audio_conversion():
    # Create directories under BASE_DIR
    output_dir = BASE_DIR / "text_outputs"
    output_dir.mkdir(exist_ok=True)
    temp_dir = BASE_DIR / "temp_audio"
    temp_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("Recording live audio...")
    recording = record_test_audio()
    temp_file = temp_dir / "temp_recording.wav"
    sf.write(str(temp_file), recording, 16000)
    processor = AudioProcessor()
    result = processor.process_call(str(temp_file))
    output_file = output_dir / f"transcription_{timestamp}.txt"
    with open(output_file, 'w') as f:
        f.write(result['text'])
    temp_file.unlink()
    temp_dir.rmdir()
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    test_audio_conversion()