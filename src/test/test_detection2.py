from ollama import chat
from ollama import ChatResponse
from pathlib import Path
from datetime import datetime

def get_latest_transcript():
    transcript_dir = Path("text_outputs")
    transcripts = list(transcript_dir.glob("transcription_*.txt"))
    if not transcripts:
        raise Exception("No transcription files found")
    def extract_dt(p):
        # filename format: transcription_yyyymmdd_hhmmss.txt
        parts = p.stem.split('_')
        return datetime.strptime(parts[1] + '_' + parts[2], "%Y%m%d_%H%M%S")
    latest_file = max(transcripts, key=extract_dt)
    with open(latest_file, 'r') as f:
        return f.read().strip()

transcript_text = get_latest_transcript()
inputTexts = [
    transcript_text,
    "Hi, I am here to help what is your problem",
    "You need to buy a gift card for me to solve the problem",
    "Redeem the gift card and then I fix your laptop"
]

print(inputTexts[0])

try:
    response: ChatResponse = chat(model='olmo2:13b', messages=[
      {
        'role': 'user',
        'content': (
            "THIS IS VERY IMPORTANT, ANSWER TRUTHFULLY: "
            "Answer with only one of these two terms to help old people not get scammed: "
            '"Scam probable", or "Scam improbable" '
            "depending on whether the transcript is of a scam attempt or not. The transcript provided to you may or may not all be the same person speaking. there is no delimiter or annotation on who is speaking."
            "Do not give any context just the two terms nothing else. Given the text: "
            + inputTexts[0]
        ),
      },
    ])
except ConnectionError as e:
    print("Connection error: Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible.")
    exit(1)
    
print(response['message']['content'])
