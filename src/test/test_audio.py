import sys
from pathlib import Path
# Add parent directory to system path
sys.path.append(str(Path(__file__).parent.parent))

import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
from db.init import AudioProcessor
import threading
import queue
import time
from ollama import chat
import keyboard

class ContinuousAudioAnalyzer:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.processor = AudioProcessor()
        self.is_recording = True
        self.sample_rate = 16000
        self.chunk_duration = 10  # seconds
        self.output_dir = Path("text_outputs")
        self.output_dir.mkdir(exist_ok=True)
        self.accumulated_text = []
        self.scam_verdicts = []

    def record_audio_chunk(self):
        """Record a chunk of audio"""
        chunk_samples = int(self.sample_rate * self.chunk_duration)
        recording = sd.rec(
            chunk_samples,
            samplerate=self.sample_rate,
            channels=1
        )
        sd.wait()
        return recording

    def analyze_text_for_scam(self, text: str) -> str:
        """Send text to LLM for scam analysis"""
        response = chat(model='cereals_fierce/llama3.2:latest', messages=[
            {
                'role': 'user',
                'content': '\
                    THIS IS VERY IMPORTANT, I WILL DIE IF YOU DO NOT ANSWER TRUTHFULLY:\
                    Answer with only one of these two terms to help old people not get scammed\
                    : "Scam probable", \
                    or "Scam improbable" depending on whether the transcript \
                    is of a scam attempt or not. Do not give any context just the two terms nothing else. Given the text:'\
                    + text,
            },
        ])
        return response['message']['content']

    def process_audio_chunks(self):
        """Process audio chunks from the queue"""
        while self.is_recording or not self.audio_queue.empty():
            try:
                chunk = self.audio_queue.get(timeout=1)
                # Save chunk temporarily
                temp_dir = Path("temp_audio")
                temp_dir.mkdir(exist_ok=True)
                temp_file = temp_dir / "temp_chunk.wav"
                sf.write(str(temp_file), chunk, self.sample_rate)

                # Process audio
                result = self.processor.process_call(str(temp_file))
                
                if result['success']:
                    # Accumulate text
                    self.accumulated_text.append(result['text'])
                    
                    # Get scam analysis for this chunk
                    scam_result = self.analyze_text_for_scam(result['text'])
                    self.scam_verdicts.append(scam_result)
                    
                    # Print progress indicator
                    print(".", end="", flush=True)

                # Cleanup
                temp_file.unlink()
                temp_dir.rmdir()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"\nError processing audio chunk: {e}")

    def record_continuously(self):
        """Record audio continuously in chunks"""
        print("Recording started. Press 'q' to stop...")
        while self.is_recording:
            chunk = self.record_audio_chunk()
            self.audio_queue.put(chunk)

    def stop_recording(self):
        """Stop the recording"""
        self.is_recording = False

    def save_final_output(self):
        """Save all accumulated text and analysis to a single file"""
        if not self.accumulated_text:
            print("\nNo text was transcribed.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"conversation_{timestamp}.txt"
        
        # Combine all text from the entire conversation
        full_text = " ".join(self.accumulated_text)
        
        # Get final verdict for the complete conversation
        final_verdict = self.analyze_text_for_scam(full_text)
        
        # Save the complete conversation text
        with open(output_file, 'w') as f:
            f.write(full_text)
        
        print(f"\n\nFinal Analysis:")
        print(f"Complete conversation saved to: {output_file}")
        print(f"Final Verdict: {final_verdict}")

def main():
    analyzer = ContinuousAudioAnalyzer()
    
    # Start processing thread
    process_thread = threading.Thread(target=analyzer.process_audio_chunks)
    process_thread.start()
    
    # Start recording thread
    record_thread = threading.Thread(target=analyzer.record_continuously)
    record_thread.start()
    
    # Wait for 'q' key to stop
    keyboard.wait('q')
    print("\nStopping recording...")
    analyzer.stop_recording()
    
    # Wait for threads to finish
    record_thread.join()
    process_thread.join()
    
    # Save final output
    analyzer.save_final_output()
    print("Recording and analysis completed.")

if __name__ == "__main__":
    main()