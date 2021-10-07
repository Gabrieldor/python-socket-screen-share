import socket
import ctypes
import os

import pygame

user32 = ctypes.windll.user32
WIDTH = user32.GetSystemMetrics(0)
HEIGHT = user32.GetSystemMetrics(1)


def recvall(conn, length):
    """ Retreive all pixels. """
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data: 
            return data
        buf += data
    return buf


def main(host='192.168.0.20', port=5000):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1920,0)
    pygame.init()
    screen = pygame.display.set_mode((int(WIDTH),HEIGHT))
    clock = pygame.time.Clock() 
    watching = True

    sock = socket.socket()
    sock.connect((host, port))
    try:
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watching = False
                    break

            # Retreive the size of the pixels length, the pixels length and pixels
            size_len = int.from_bytes(sock.recv(1), byteorder='big')
            size = int.from_bytes(sock.recv(size_len), byteorder='big')
            pixels = recvall(sock, size)

            # Create the Surface from raw pixels
            img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')
            img = pygame.transform.scale(img, (int(WIDTH/2), HEIGHT))

            # Display the picture
            screen.blit(img, (0, 0))
            screen.blit(img, (int(WIDTH/2), 0))
            
            pygame.display.flip()
            clock.tick(240)
    finally:
        sock.close()


if __name__ == '__main__':
    main()