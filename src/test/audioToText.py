from RealtimeSTT import AudioToTextRecorder

def process_text(text):
    with open("./text_outputs/transcription_20250201_155748.txt", "a", encoding="utf-8") as file:
        file.write(text + "\n")  # Append the text to the file

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)