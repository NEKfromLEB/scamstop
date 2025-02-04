import socket
from ollama import chat, ChatResponse
from pathlib import Path
from datetime import datetime
import subprocess, time, os

# Define BASE_DIR relative to this file
BASE_DIR = Path(__file__).resolve().parent

text_file = ""
transcript_text = ""
file_path = ""
modelName = "olmo2:13b"

def get_latest_transcript():
    global text_file
    # Use BASE_DIR for transcripts directory
    transcript_dir = BASE_DIR / "text_outputs"
    transcripts = list(transcript_dir.glob("transcription_*.txt"))
    if not transcripts:
        raise Exception("No transcription files found")
    def extract_dt(p):
        # filename format: transcription_yyyymmdd_hhmmss.txt
        parts = p.stem.split('_')
        return datetime.strptime(parts[1] + '_' + parts[2], "%Y%m%d_%H%M%S")
    text_file = max(transcripts, key=extract_dt)
    with open(text_file, 'r') as f:
        return f.read().strip()

def wait_for_new_transcript(interval=1):
    global text_file, transcript_text
    last_known_file = text_file
    while True:
        transcript_dir = BASE_DIR / "text_outputs"
        transcripts = list(transcript_dir.glob("transcription_*.txt"))
        if not transcripts:
            time.sleep(interval)
            continue
        newest_file = max(transcripts, key=lambda f: f.stat().st_mtime)
        if newest_file != last_known_file:
            print("New transcript file found:", newest_file)
            text_file = newest_file
            transcript_text = get_latest_transcript()
            return True
        time.sleep(interval)

def start_ollama():
    print("Ollama is not running; starting headless...")
    # NEW: Launch ollama headlessly in the background.
    subprocess.Popen("ollama serve; sleep 3; ollama run olmo2:13b", shell=True, 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)

def is_ollama_running(port=11434):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('127.0.0.1', port))
        s.close()
        return False
    except socket.error:
        return True

def call_llm():
    global transcript_text
    transcript_text = get_latest_transcript()  # NEW: Force a fresh read from the file
    print("Sending this text to LLM:\n", transcript_text)  # NEW: log text to console
    print(transcript_text)
    try:
        response: ChatResponse = chat(model=modelName, messages=[
            {
                'role': 'user',
                'content': (
                    "THIS IS VERY IMPORTANT, ANSWER TRUTHFULLY: "
                    "Answer with only one of these two terms to help old people not get scammed: "
                    '"Scam probable", or "Scam improbable" '
                    "depending on whether the transcript is of a scam attempt or not. "
                    "Do not give any context just the two terms nothing else. Given the text: "
                    + transcript_text
                ),
            },
        ])
    except Exception as e:
        if ("llama runner process" in str(e) or "broken pipe" in str(e)):
            start_ollama()
            time.sleep(10)
            response: ChatResponse = chat(model=modelName, messages=[
                {
                    'role': 'user',
                    'content': (
                        "THIS IS VERY IMPORTANT, ANSWER TRUTHFULLY: "
                        "Answer with only one of these two terms to help old people not get scammed: "
                        '"Scam probable", or "Scam improbable" '
                        "depending on whether the transcript is of a scam attempt or not. "
                        "Do not give any context just the two terms nothing else. Given the text: "
                        + transcript_text
                    ),
                },
            ])
        else:
            raise
    result_content = response['message']['content']
    print(result_content)
    return result_content  # NEW: return the result

if __name__ == "__main__":
    # Get transcript and set file_path based on BASE_DIR
    transcript_text = get_latest_transcript()
    file_path = str(text_file)
    if not is_ollama_running():
        start_ollama()
    call_llm()

    while True:
        wait_for_new_transcript()  # Wait for a newly created file
        call_llm()


