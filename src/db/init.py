import speech_recognition as sr
from transformers import AutoTokenizer, AutoModel
import torch
import soundfile as sf
from typing import Dict, Any
import json

class AudioProcessor:
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        # Initialize transformer model for embeddings
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def audio_to_text(self, audio_path: str) -> str:
        """Convert audio file to text using speech recognition."""
        try:
            # Load audio file
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                # Convert speech to text
                text = self.recognizer.recognize_google(audio)
                return text
        except Exception as e:
            print(f"Error in speech recognition: {str(e)}")
            return ""

    def create_embedding(self, text: str) -> torch.Tensor:
        """Create embeddings from text using transformer model."""
        # Tokenize and create embedding
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Use mean pooling to get sentence embedding
        embedding = torch.mean(outputs.last_hidden_state, dim=1)
        return embedding

    def process_call(self, audio_path: str) -> Dict[str, Any]:
        """Process a phone call recording: convert to text and create embedding."""
        # Convert audio to text
        text = self.audio_to_text(audio_path)
        
        # Create embedding if text was successfully extracted
        if text:
            embedding = self.create_embedding(text)
            return {
                "text": text,
                "embedding": embedding.tolist(),
                "audio_path": audio_path,
                "success": True
            }
        else:
            return {
                "text": "",
                "embedding": None,
                "audio_path": audio_path,
                "success": False
            }

# Example usage
if __name__ == "__main__":
    processor = AudioProcessor()
    result = processor.process_call("path/to/your/audio/file.wav")
    print(json.dumps(result, indent=2))