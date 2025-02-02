from flask import Flask, jsonify
import subprocess
import sys
import os

# Import detection module (ensure your PYTHONPATH is set correctly)
from src.test import detection

# Updated: Serve static files from the 'frontend' directory
app = Flask(__name__, static_folder="frontend", static_url_path="")

rec_process = None  # NEW: Global for recording process

# Updated: Serve the index page using Flask's static file serving
@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("display.html")

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global rec_process
    if rec_process is None:
        rec_process = subprocess.Popen([sys.executable, "src/test/audioToText.py"])
        return jsonify({"status": "recording started"})
    else:
        return jsonify({"status": "already recording"})

# NEW: Stop endpoint to kill the recording process
@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global rec_process
    if rec_process is not None:
        rec_process.terminate()  # Use terminate instead of kill
        rec_process.wait()       # Wait for process to clean up
        rec_process = None
        return jsonify({"status": "recording stopped"})
    else:
        return jsonify({"status": "not recording"})

@app.route('/detect_scam', methods=['GET'])
def detect_scam():
    # Call the detection function and return its result
    result = detection.call_llm()
    return jsonify({"detection_result": result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
