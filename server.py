from socket import socket


import socket

def main(host='192.168.0.20', port=5000):
    
    sock = socket.socket()
    sock.bind((host, port))
    try:
        sock.listen(1)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            while True:
                conn.sendall('TESTE\n'.encode())
    finally:
        sock.close()


if __name__ == '__main__':
    main()