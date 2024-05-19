from flask import Flask, request, jsonify, render_template
import os
import threading
from dotenv import load_dotenv
import whisper
import logging

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Optional: Define port in config.py (if using)
# from config import PORT

# Get the port from the environment variable or use 4000 as default
port = int(os.environ.get("PORT", 3000))

# Load the Whisper model for transcription
model = whisper.load_model("base")

# ... rest of your code (routes, functions, etc.)
# Define a function to record audio from the microphone
def record_audio(filename, duration):
    os.system(f"arecord -d {duration} -f cd -t wav {filename}")

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Check if the 'audio' file is in the request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'})

        audio_file = request.files['audio']
        audio_file.save("recorded_audio.wav")
        
        # Transcribe the audio using the pre-loaded Whisper model
        result = model.transcribe("recorded_audio.wav")
        transcription = result["text"]

        return jsonify({'transcription': transcription})

    except Exception as e:
        return jsonify({'error': str(e)})

# ... (other definitions if needed)

if __name__ == '__main__':
  # Use Gunicorn command instead of app.run
  # Replace 'appcode' with your actual filename
  os.system(f"gunicorn gunicode:app --bind 0.0.0.0:{port}")
