import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('52.78.37.233', 8000)

sock.connect(server_address)