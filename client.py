import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.192.137',12345))

msg = s.recv(10240000)
if msg[0] == 49:
    print(msg[1:].decode('utf-8'))
else:
    with open('gay.png','wb') as f:
        f.write(msg)

input()