from flask import Flask, render_template, jsonify
import cv2
import numpy as np
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)

# Allow connections from any origin (you can replace "*" with specific origins)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize OpenCV
cap = cv2.VideoCapture(0)

def detect_gesture(frame):
    # This is a placeholder function.
    # Replace this with actual gesture detection logic using OpenCV or other methods.

    # For now, let's just detect simple gestures: hand raised or closed fist (for simplicity)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Your gesture detection logic goes here.
    # We'll return dummy values for now (just for demo purposes)
    if np.random.rand() > 0.7:
        return "running"
    elif np.random.rand() > 0.3:
        return "jumping"
    else:
        return "walking"

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('get_gesture')
def handle_gesture_request():
    ret, frame = cap.read()
    if not ret:
        return
    gesture = detect_gesture(frame)
    emit('gesture', {'gesture': gesture})
    time.sleep(0.1)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
