from flask import Flask, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv
import logging
from threading import Event
from banter_assignment.get_transcription import on_disconnect , start_transcription_loop

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)

# Track transcription state
transcribing = False
transcription_event = Event()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('disconnect')
def handle_disconnect():
    socketio.start_background_task(target=on_disconnect)

@socketio.on('toggle_transcription')
def toggle_transcription(data):
    global transcribing
    action = data.get('action')

    if action == 'start' and not transcribing:
        # Start transcription
        transcribing = True
        socketio.start_background_task(target=start_transcription_loop, transcribing=transcribing,  transcription_event=transcription_event , socketio=socketio)
    elif action == 'stop' and transcribing:
        # Stop transcription
        transcribing = False
        transcription_event.set()

if __name__ == '__main__':
    logging.info("Starting SocketIO server.")
    socketio.run(app, debug=True)