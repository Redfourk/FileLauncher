import socket

# Connect
s = socket.socket()
s.connect(('1.2.3.4', 80))

# Read and Send
with open('test.txt', 'rb') as f:
    s.sendall(f.read())
s.close()

