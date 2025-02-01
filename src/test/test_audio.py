import sys
from pathlib import Path
# Add parent directory to system path
sys.path.append(str(Path(__file__).parent.parent))

import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
from db.init import AudioProcessor

def record_test_audio(duration=40, sample_rate=16000):
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
    # Create output directory for text files
    output_dir = Path("text_outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create temporary directory for audio files
    temp_dir = Path("temp_audio")
    temp_dir.mkdir(exist_ok=True)
    
    # Record live audio
    print("Recording live audio...")
    recording = record_test_audio()
    temp_file = temp_dir / "temp_recording.wav"
    sf.write(str(temp_file), recording, 16000)
    
    # Process audio file
    processor = AudioProcessor()
    result = processor.process_call(str(temp_file))
    
    # Save only the transcribed text
    output_file = output_dir / f"transcription_{timestamp}.txt"
    with open(output_file, 'w') as f:
        f.write(result['text'])
    
    # Clean up temporary audio files
    temp_file.unlink()
    temp_dir.rmdir()
    
    # Print results to console
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    test_audio_conversion()