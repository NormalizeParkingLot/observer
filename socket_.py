import socket
import time

host = "2001:db8::67"
port = 61617
msg = 1

server_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
server_socket.connect((host, port))

# for i in range(10):
server_socket.send(msg.to_bytes(1, 'big'))
    # time.sleep(5)

server_socket.close()