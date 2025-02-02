import socket
from ollama import chat
from ollama import ChatResponse
from pathlib import Path
from datetime import datetime
import subprocess, time
import os

#Needs to be run from ../scamstop directory

text_file = ""
transcript_text = ""
file_path = ""
modelName = "cereals_fierce/llama3.2:latest"

def get_latest_transcript():
    global text_file
    transcript_dir = Path("scamstop/src/test/text_outputs")
    
    # Get a list of transcript files with full paths
    transcripts = list(transcript_dir.glob("transcription_*.txt"))
    
    if not transcripts:
        raise Exception("No transcription files found")

    def extract_dt(p):
        # filename format: transcription_yyyymmdd_hhmmss.txt
        parts = p.stem.split('_')
        return datetime.strptime(parts[1] + '_' + parts[2], "%Y%m%d_%H%M%S")

    # Find the latest transcription file
    text_file = max(transcripts, key=extract_dt)

    # Read the content of the latest file
    with open(text_file, 'r') as f:
        return f.read().strip()
    
def detect_file_changes(interval=1):
    global transcript_text

    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            print("File has changed!")
            transcript_text = get_latest_transcript()
            last_modified = current_modified
            return True
        time.sleep(interval)

def start_ollama():
    print("Ollama is not running; starting...")
    subprocess.Popen(["ollama", "serve"])
    time.sleep(3)
    subprocess.Popen(["ollama", "run", "olmo2:13b"])
    time.sleep(5)

def is_ollama_running(port=11434):
    """Return True if Ollama is already running on the specified port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('127.0.0.1', port))
        s.close()
        return False
    except socket.error:
        return True
    
def call_llm():
    print(transcript_text)
    try:
        response: ChatResponse = chat(model=modelName, messages=[
        {
            'role': 'user',
            'content': (
                "THIS IS VERY IMPORTANT, ANSWER TRUTHFULLY: "
                "Answer with only one of these two terms to help old people not get scammed: "
                '"Scam probable", or "Scam improbable" '
                "depending on whether the transcript is of a scam attempt or not. The transcript provided to you may or may not all be the same person speaking. there is no delimiter or annotation on who is speaking."
                "Do not give any context just the two terms nothing else. Given the text: "
                + transcript_text
            ),
        },
        ])
    except Exception as e:
        if ("llama runner process" in str(e) or "broken pipe" in str(e)):
            start_ollama()
            # Wait a bit longer before retrying
            import time
            time.sleep(10)
            response: ChatResponse = chat(model=modelName, messages=[
            {
                'role': 'user',
                'content': (
                    "THIS IS VERY IMPORTANT, ANSWER TRUTHFULLY: "
                    "Answer with only one of these two terms to help old people not get scammed: "
                    '"Scam probable", or "Scam improbable" '
                    "depending on whether the transcript is of a scam attempt or not. The transcript provided to you may or may not all be the same person speaking. there is no delimiter or annotation on who is speaking."
                    "Do not give any context just the two terms nothing else. Given the text: "
                    + transcript_text
                ),
            },
            ])
        else:
            raise

    print(response['message']['content'])


if not is_ollama_running():
    start_ollama()

transcript_text = get_latest_transcript()
file_path = './' + str(text_file)
call_llm()


while True:
    detect_file_changes()#wait for file to change then call llm
    call_llm()


