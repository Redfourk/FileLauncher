import socket

# Connect
s = socket.socket()
s.connect(('0.0.0.0', 5001))

# Read and Send
with open('layout.tcss', 'rb') as f:
    s.sendall(f.read())
s.close()
