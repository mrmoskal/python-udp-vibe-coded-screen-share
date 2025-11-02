import cv2
import socket
import threading
# import numpy as np
#
# # Server code
# def server():
#     # Create a UDP socket
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     server_socket.bind(('localhost', 5000))
#
#     print('Server started. Waiting for client connection...')
#
#     while True:
#         # Receive data from the client
#         data, addr = server_socket.recvfrom(65536)
#
#         # Decode the image data
#         img = np.frombuffer(data, dtype=np.uint8)
#         img = cv2.imdecode(img, cv2.IMREAD_COLOR)
#
#         # Display the received image
#         cv2.imshow('Server', img)
#         cv2.waitKey(1)


# Client code
import mss
import cv2
import socket
import threading
import numpy as np


# Client code
def client():
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ⚠️ IMPORTANT: Set a fixed, aggressive JPEG compression quality
    # to keep packet sizes small and prevent WinError 10040.
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]

    # Initialize the screen capture tool
    sct = mss.mss()

    # Define the screen area to capture (e.g., the primary monitor)
    # This dictionary defines the bounding box for the capture.
    monitor = sct.monitors[1]  # Use monitor 1 (usually the primary)

    # Optional: Define a smaller area for faster transmission
    # monitor = {"top": 100, "left": 100, "width": 800, "height": 600}

    while True:
        # 1. Capture the screen content using mss
        sct_img = sct.grab(monitor)

        # 2. Convert the captured image (an mss object) into a NumPy array (OpenCV format)
        # Use np.array and cv2.IMREAD_COLOR to ensure correct format
        # The 'bgr' property ensures the correct color channel order for OpenCV
        frame = np.array(sct_img, dtype=np.uint8)

        # NOTE: mss captures in BGRA, so you might want to convert it to BGR for smaller size:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # 3. Encode the frame as a JPEG image
        ret, jpeg = cv2.imencode('.jpg', frame, encode_param)

        # 4. Send the image data to the server (listening on port 5000)
        if ret:
            client_socket.sendto(jpeg.tobytes(), ('localhost', 5000))

        # Wait for a short time to limit the frame rate
        cv2.waitKey(1)


if __name__ == '__main__':
    # Run the server and client in separate threads or processes
    # server_thread = threading.Thread(target=server)  # server thread
    client_thread = threading.Thread(target=client)  # client thread

    # server_thread.start()
    client_thread.start()

