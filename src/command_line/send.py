import socket

# Connect
s = socket.socket()
s.connect(('172.31.11.167', 5001))

# Read and Send
with open('my_data.zip', 'rb') as f:
    s.sendall(f.read())
s.close()
