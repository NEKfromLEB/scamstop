import sounddevice as sd
import soundfile as sf
from pathlib import Path
from db.init import ScamCallDetector

def record_and_analyze(duration=10):
    """Record audio and analyze it for scam indicators"""
    # Setup
    sample_rate = 16000
    test_dir = Path("test_audio")
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / "scam_test_recording.wav"
    
    # Record audio
    print(f"\nRecording for {duration} seconds... Please speak into your microphone.")
    print("Try saying something like a scam call or a normal conversation.")
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1
    )
    sd.wait()
    
    # Save recording
    sf.write(str(test_file), recording, sample_rate)
    print("\nRecording saved!")
    
    # Analyze the recording
    detector = ScamCallDetector()
    result = detector.process_call(str(test_file))
    
    # Print results
    print("\n=== Analysis Results ===")
    if result["success"]:
        print(f"\nTranscribed Text: {result['text']}")
        print(f"\nScam Probability: {result['scam_probability']:.2%}")
        print(f"Risk Level: {result['risk_level']}")
        print("\nDetected Scam Indicators:")
        if result['matched_indicators']:
            for indicator in result['matched_indicators']:
                print(f"- {indicator}")
        else:
            print("- No specific scam indicators detected")
    else:
        print("Failed to process the audio. Please try again.")

def test_sample_texts():
    """Test the scam detector with predefined text samples"""
    print("\n=== Testing Sample Texts ===")
    
    detector = ScamCallDetector()
    test_cases = [
        "Hi, this is the IRS calling. Your social security number has been suspended due to suspicious activity.",
        "Hello, I'm calling about your car's extended warranty which is about to expire. This is urgent.",
        "Hi, this is John from the local dentist office calling to confirm your appointment tomorrow at 2 PM.",
        "We've detected suspicious transactions in your bank account. We need your verification immediately."
    ]
    
    for text in test_cases:
        print("\n---")
        print(f"Test text: {text}")
        result = detector.analyze_scam_probability(text)
        print(f"Scam Probability: {result['scam_probability']:.2%}")
        print(f"Risk Level: {result['risk_level']}")
        print("Matched Indicators:", ', '.join(result['matched_indicators']) if result['matched_indicators'] else "None")

if __name__ == "__main__":
    while True:
        print("\nScam Call Detection Test")
        print("1. Record and analyze live audio")
        print("2. Test with sample texts")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            record_and_analyze()
        elif choice == "2":
            test_sample_texts()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")