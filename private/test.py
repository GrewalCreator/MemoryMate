import cv2
import requests
import time

def send_camera_feed_to_backend(camera_index):
    """
    Captures video frames from the laptop camera and sends them to the backend's live-feed endpoint.
    """
    backend_url = 'http://127.0.0.1:5000/api/live-feed'  # Update with your backend's URL
    camera = cv2.VideoCapture(camera_index)  # Open the default camera

    if not camera.isOpened():
        print("Unable to access the camera")
        return

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Failed to read frame from camera")
                break

            # Encode the frame as a JPEG image
            _, buffer = cv2.imencode('.jpg', frame)

            # Send the frame to the backend
            response = requests.post(
                backend_url,
                files={'video': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
            )

            if response.status_code == 200:
                print("Frame sent successfully")
            else:
                print(f"Failed to send frame: {response.status_code}, {response.text}")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        camera.release()
        print("Camera released")

if __name__ == "__main__":
    # 0 -> Default
    # 1 & Above -> Connected Webcams
    send_camera_feed_to_backend(1)