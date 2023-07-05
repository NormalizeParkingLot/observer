import socket
import time

host = "2001:db8::4"
port = 61617
msg = "message"

server_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
server_socket.connect((host, port))

for i in range(10):
    server_socket.send(msg.encode())
    time.sleep(5)

server_socket.close()