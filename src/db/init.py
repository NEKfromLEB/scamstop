import speech_recognition as sr
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
import torch
import soundfile as sf
from typing import Dict, Any
import json
import torch.nn.functional as F

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

    def extract_advanced_features(self, text: str) -> Dict[str, Any]:
        return {
            "urgency_markers": self._detect_urgency(text),
            "monetary_mentions": self._detect_money_references(text),
            "pressure_tactics": self._detect_pressure(text),
            "emotional_manipulation": self._detect_emotional_triggers(text)
        }

class ScamCallDetector(AudioProcessor):
    def __init__(self):
        super().__init__()
        # Load a model fine-tuned for scam detection
        # Using roberta-base as an example, but you should fine-tune it on scam data
        self.scam_tokenizer = AutoTokenizer.from_pretrained("roberta-base")
        self.scam_model = AutoModelForSequenceClassification.from_pretrained("roberta-base")
        
        # Common scam indicators
        self.scam_indicators = [
            "urgent action required",
            "social security",
            "gift card",
            "warranty expiring",
            "bank account suspicious",
            "irs",
            "tax fraud",
            "legal action",
            "arrest warrant",
            "verify identity"
        ]

    def analyze_scam_probability(self, text: str) -> Dict[str, Any]:
        """Analyze text for scam indicators and return probability."""
        # Check for common scam phrases
        indicator_matches = [
            indicator for indicator in self.scam_indicators 
            if indicator in text.lower()
        ]
        
        # Get model prediction
        inputs = self.scam_tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.scam_model(**inputs)
            probabilities = F.softmax(outputs.logits, dim=1)
            scam_probability = probabilities[0][1].item()  # Assuming binary classification
        
        return {
            "scam_probability": scam_probability,
            "matched_indicators": indicator_matches,
            "risk_level": "high" if scam_probability > 0.7 else "medium" if scam_probability > 0.4 else "low"
        }

    def process_call(self, audio_path: str) -> Dict[str, Any]:
        """Enhanced process_call with scam detection"""
        # Get basic processing results
        result = super().process_call(audio_path)
        
        if result["success"]:
            # Add scam analysis
            scam_analysis = self.analyze_scam_probability(result["text"])
            result.update(scam_analysis)
        
        return result

# Example usage
if __name__ == "__main__":
    processor = ScamCallDetector()
    result = processor.process_call("path/to/your/audio/file.wav")
    print(json.dumps(result, indent=2))