import json
import threading

import pyttsx3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Initial prompt and sequence of tasks
tasks = [
    "firstly give report on tires",
    "give report on engine",
    "give report on brakes",
    "give report on battery",
]

# Initialize task index
task_index = 0

# Initialize TTS engine
tts_engine = pyttsx3.init()

def speak_text(text):
    def run_speech():
        tts_engine.say(text)
        tts_engine.runAndWait()
    
    threading.Thread(target=run_speech).start()

# Route for the main page
@app.route('/')
def index():
    global task_index
    task_index = 0  # Reset to the first task
    prompt = tasks[task_index]
    speak_text(prompt)
    return render_template('index.html', prompt=prompt)

# Route to process the voice input
@app.route('/process', methods=['POST'])
def process_input():
    global task_index
    user_input = request.json.get("input", "").lower()

    if "next" in user_input:
        task_index += 1
        if task_index < len(tasks):
            prompt = tasks[task_index]
            speak_text(prompt)
            return jsonify({"prompt": prompt})
        else:
            prompt = "Inspection completed. Thank you!"
            speak_text(prompt)
            return jsonify({"prompt": prompt})
    else:
        return jsonify({"prompt": "Please write 'next' to continue."})

# Route to save the inspection report
@app.route('/save_report', methods=['POST'])
def save_report():
    data = request.json
    with open("inspection_report.json", "w") as file:
        json.dump(data, file)
    return jsonify({"status": "saved"})

if __name__ == '__main__':
    app.run(debug=True)
