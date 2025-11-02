
import cv2
import socket
import threading
import numpy as np
from flask import Flask, Response

# --- Global Storage for the latest received frame ---
# This will hold the raw JPEG bytes received from the UDP client.
latest_frame = None
latest_frame_lock = threading.Lock()

# --- Flask Web Server Setup ---
app = Flask(__name__)


@app.route('/api/screen-capture')
def screen_capture():
    """
    HTTP endpoint requested by the HTML <script> tag.
    It returns the latest frame received from the UDP client.
    """
    global latest_frame
    with latest_frame_lock:
        if latest_frame is None:
            # Return a 204 No Content or similar if no frame has arrived yet
            return Response("No frame yet", status=204)

        # 1. Get the raw JPEG bytes
        jpeg_bytes = latest_frame

        # 2. Return the image bytes with the correct MIME type (image/jpeg)
        return Response(
            jpeg_bytes,
            mimetype='image/jpeg'
        )


# --- UDP Server Receiver Function ---
def udp_receiver():
    """
    The thread that continuously listens for UDP packets (frames)
    from the original Python client.
    """
    global latest_frame

    # Use a safe buffer size (65507 is max UDP data size)
    # This must be large enough to receive the entire JPEG frame!
    BUFFER_SIZE = 65536

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # It's better to bind to '0.0.0.0' for external access,
    # but 'localhost' works for testing on the same machine.
    server_socket.bind(('localhost', 5000))

    print('UDP Receiver started on port 5000...')

    while True:
        try:
            # Receive data from the client (this is the JPEG data)
            data, addr = server_socket.recvfrom(BUFFER_SIZE)

            # Store the raw data bytes
            with latest_frame_lock:
                latest_frame = data

            # Optional: Add a check here for the frame size to prevent the OSError
            # by confirming the client is using compression (as discussed earlier).

        except Exception as e:
            print(f"Error in UDP receiver: {e}")
            break


# --- Main Execution ---
if __name__ == '__main__':
    # 1. Start the UDP receiver thread
    receiver_thread = threading.Thread(target=udp_receiver, daemon=True)
    receiver_thread.start()

    # 2. Start the Flask web server (this is the main thread)
    print('Starting Flask web server on http://127.0.0.1:8080...')
    # Use port 8080 or any other free port
    app.run(host='0.0.0.0', port=8080, debug=False)