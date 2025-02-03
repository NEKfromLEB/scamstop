# scamstop


# Inspiration
ScamStop was inspired by a personal experience—my grandmother fell victim to a phone scam by fraudsters impersonating a utility company. This made us realize how vulnerable people, especially elders, are to these deceptive tactics. We wanted to build a tool that could intervene in real time, preventing these scams before any damage is done.

# What it does
ScamStop listens to ongoing conversations and analyzes them in real time to detect scam patterns. Using AI-powered language processing, it identifies warning signs such as urgency, threats, or requests for sensitive information. If a scam is detected, the system issues an alert, helping users recognize fraudulent calls before they fall victim.

# How we built it
Frontend: HTML/CSS with vanilla JavaScript
Backend: Flask server managing audio processing and ML model interactions
Real-time Speech-to-Text: RealtimeSTT for continuous transcription
AI Model: Ollama running locally with olmo2:13b for scam detection (can use different models)
Process Management: Python subprocess handling for continuous recording and analysis

# Challenges we ran into
Managing microphone resources between processes
Implementing real-time updates without overwhelming the system
Coordinating multiple processes (recording, transcription, and detection)
Ensuring reliable communication between frontend and backend components
Balancing speed and accuracy in scam detection
RELIABILITY

# Accomplishments that we're proud of
Implemented continuous speech-to-text processing
Built a web interface for monitoring
Developed a system that can help protect vulnerable populations
Successfully integrated local LLM for privacy-conscious analysis

# What we learned
Real-time audio processing techniques
Process management in Python
Frontend-backend communication patterns
Local LLM integration

# What's next for StopScam
Improve detection accuracy with our own model
Add support for multiple languages
Implement call recording for evidence
Create mobile applications for wider accessibility (privacy features may make this hard)
Add more sophisticated scam pattern recognition
