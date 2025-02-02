from RealtimeSTT import AudioToTextRecorder
from datetime import datetime
from pathlib import Path

# NEW: Define BASE_DIR to ensure correct transcript directory regardless of the working directory
BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "text_outputs"
output_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
transcript_file = output_dir / f"transcription_{timestamp}.txt"

def process_text(text):
    # Append the text to the new transcript file
    with open(transcript_file, "a", encoding="utf-8") as file:
        file.write(text + "\n")

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)