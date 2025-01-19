import cv2
import requests
import threading
import time
import queue

# Configuration
backend_url = 'http://127.0.0.1:5000/api/live-feed'
camera_index = 0  # Default camera
frame_queue = queue.Queue(maxsize=100)  # Queue to store frames for processing
stop_event = threading.Event()

def capture_frames():
    """
    Capture frames from the camera and push them into the queue.
    """
    camera = cv2.VideoCapture(camera_index)
    camera.set(cv2.CAP_PROP_FPS, 60)  # Attempt to set camera FPS to 60
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not camera.isOpened():
        print("Unable to access the camera")
        return

    print("Capturing frames at 60 FPS...")
    while not stop_event.is_set():
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Drop frames if queue is full to maintain real-time processing
        if not frame_queue.full():
            frame_queue.put(frame)

    camera.release()
    print("Camera released")

def send_frames():
    """
    Retrieve frames from the queue and send them to the backend.
    """
    while not stop_event.is_set() or not frame_queue.empty():
        if not frame_queue.empty():
            frame = frame_queue.get()

            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            files = {'video': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
            
            try:
                response = requests.post(backend_url, files=files, timeout=10)
                if response.status_code == 200:
                    print("Frame sent successfully")
                else:
                    print(f"Failed to send frame: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")

            frame_queue.task_done()

        else:
            time.sleep(0.001)  # Small sleep to prevent CPU overuse

if __name__ == "__main__":
    try:
        # Start frame capture and sending in separate threads
        capture_thread = threading.Thread(target=capture_frames, daemon=True)
        send_thread = threading.Thread(target=send_frames, daemon=True)

        capture_thread.start()
        send_thread.start()

        # Run for a specific duration (e.g., 30 seconds) or until user interrupt
        #time.sleep(30)  # Run for 30 seconds (adjust as needed)

    except KeyboardInterrupt:
        print("\nStopped by user")
    
    finally:
        stop_event.set()
        capture_thread.join()
        send_thread.join()
        print("Exiting gracefully")
