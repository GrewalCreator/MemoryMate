from flask import Flask, request
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
from threading import Lock
from groqAI import facial_recognition

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

latest_frame = None
frame_lock = Lock()

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('request_frame')
def handle_frame_request():
    global latest_frame
    with frame_lock:
        if latest_frame is not None:
            emit('new_frame', latest_frame)

def process_frame(frame):
    global latest_frame
    # Process the frame (e.g., facial recognition)
    processed_frame = facial_recognition(frame)
    _, buffer = cv2.imencode('.jpg', processed_frame)
    with frame_lock:
        latest_frame = buffer.tobytes()
    socketio.emit('new_frame', latest_frame)

@app.route('/api/live-feed', methods=['POST'])
def live_feed():
    video_file = request.files['video']
    video_stream = video_file.read()
    nparr = np.frombuffer(video_stream, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is not None:
        process_frame(frame)
    return "Frame received and processed", 200


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
