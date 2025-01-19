import cv2
import requests
import time

def send_camera_feed_to_backend(camera_index=0):
    backend_url = 'http://127.0.0.1:5000/api/live-feed'  # Ensure correct backend URL

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

            files = {'video': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
            try:
                response = requests.post(backend_url, files=files, timeout=10)
                if response.status_code == 200:
                    print("Frame sent successfully")
                else:
                    print(f"Failed to send frame: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")

            time.sleep(1)  # Control the frame sending rate
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        camera.release()
        print("Camera released")

if __name__ == "__main__":
    send_camera_feed_to_backend()
