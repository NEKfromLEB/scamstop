from flask import Flask, jsonify
from flask_cors import CORS  # NEW: Import CORS
import subprocess
import sys
import os
import time  # NEW: Import time for delay

# Import detection module (ensure your PYTHONPATH is set correctly)
from src.test import detection

# Updated: Serve static files from the 'frontend' directory
app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)  # NEW: Enable CORS

rec_process = None  # NEW: Global for recording process
detect_process = None  # NEW: Global for detection process

# Updated: Serve the index page using Flask's static file serving
@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("display.html")

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global rec_process, detect_process
    if rec_process is None:
        print("Starting recording process...")
        rec_process = subprocess.Popen([sys.executable, "src/test/audioToText.py"])
        time.sleep(5)  # NEW: Add delay before starting detection
        print("Starting detection process...")
        detect_process = subprocess.Popen([sys.executable, "src/test/detection.py"])
        return jsonify({"status": "recording and detection started"})
    else:
        return jsonify({"status": "already recording"})

# NEW: Stop endpoint to kill the recording and detection processes
@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global rec_process, detect_process
    if rec_process is not None:
        print("Stopping recording process...")
        rec_process.terminate()  # Use terminate instead of kill
        rec_process.wait()       # Wait for process to clean up
        rec_process = None
    if detect_process is not None:
        print("Stopping detection process...")
        detect_process.terminate()  # Use terminate instead of kill
        detect_process.wait()       # Wait for process to clean up
        detect_process = None
    return jsonify({"status": "recording and detection stopped"})

@app.route('/detect_scam', methods=['GET'])
def detect_scam():
    try:
        result = detection.call_llm()
        response = jsonify({"detection_result": result})
        response.headers.add('Access-Control-Allow-Origin', '*')  # NEW: Ensure CORS headers
        return response
    except Exception as e:
        print(f"Error in detect_scam: {str(e)}")
        return jsonify({"detection_result": str(e)})

if __name__ == "__main__":
    # NEW: Ensure Ollama is running before starting the server
    if not detection.is_ollama_running():
        detection.start_ollama()
    app.run(debug=True, port=5000)
