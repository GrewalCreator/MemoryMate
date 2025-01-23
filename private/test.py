import cv2
import requests
import time

def send_camera_feed_to_backend(camera_index=0, target_fps=30, max_retries=3, retry_delay=2):
    backend_url = 'http://localhost:5000/api/live-feed'  # Ensure correct backend URL

    camera = cv2.VideoCapture(camera_index)  # Open the default camera
    if not camera.isOpened():
        print("Unable to access the camera")
        return

    # Calculate frame interval for target FPS
    frame_interval = 1.0 / target_fps
    prev_time = time.time()

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Failed to read frame from camera")
                break

            current_time = time.time()
            elapsed_time = current_time - prev_time

            if elapsed_time >= frame_interval:
                prev_time = current_time

                # Encode the frame as a JPEG image
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

                files = {'video': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
                success = False

                for attempt in range(max_retries):
                    try:
                        response = requests.post(backend_url, files=files, timeout=5)
                        if response.status_code == 200:
                            print("Frame sent successfully")
                            success = True
                            break  # Exit retry loop on success
                        else:
                            print(f"Failed to send frame (attempt {attempt + 1}): {response.status_code}, {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"Request failed (attempt {attempt + 1}): {e}")
                        time.sleep(retry_delay)  # Wait before retrying

                if not success:
                    print("Max retries reached. Skipping this frame to avoid congestion.")

    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("Camera released")

if __name__ == "__main__":
    send_camera_feed_to_backend()
