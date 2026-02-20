import socket

# Connect
s = socket.socket()
s.connect(('10.53.132.146', 5001))

# Read and Send
with open('test.txt', 'rb') as f:
    s.sendall(f.read())
s.close()

# 172.31.11.167