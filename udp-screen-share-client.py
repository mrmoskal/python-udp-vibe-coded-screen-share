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
def client():
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Capture the screen
    screen = cv2.VideoCapture(0)

    # Use a lower quality setting (e.g., 20 out of 100)
    # The 'cv2.IMWRITE_JPEG_QUALITY' flag is used with a value between 0-100.
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]

    while True:
        ret, frame = screen.read()

        # Encode the frame with aggressive compression
        _, jpeg = cv2.imencode('.jpg', frame, encode_param)

        # CHECK THE SIZE (optional but recommended for debugging)
        # print(f"Packet size: {len(jpeg.tobytes())} bytes")

        # Send the image data to the server
        client_socket.sendto(jpeg.tobytes(), ('localhost', 5000))

        # Wait for a short time to limit the frame rate
        cv2.waitKey(1)


if __name__ == '__main__':
    # Run the server and client in separate threads or processes
    # server_thread = threading.Thread(target=server)  # server thread
    client_thread = threading.Thread(target=client)  # client thread

    # server_thread.start()
    client_thread.start()

