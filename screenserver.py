import socket
from threading import Thread
import ctypes

from mss import mss


user32 = ctypes.windll.user32
WIDTH = user32.GetSystemMetrics(0)
HEIGHT = user32.GetSystemMetrics(1)


def retreive_screenshot(conn):
    with mss() as sct:
        # The region to capture
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while 'recording':
            # Capture the screen
            img = sct.grab(rect)
            # Tweak the compression level here (0-9)

            # Send the size of the pixels length
            size = len(img.rgb)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            # Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            # Send pixels
            conn.sendall(img.rgb)

def main(host='192.168.0.20', port=5000):
    sock = socket.socket()
    sock.bind((host, port))
    try:
        sock.listen(2)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=retreive_screenshot, args=(conn,))
            thread.start()
    finally:
        sock.close()


if __name__ == '__main__':
    main()