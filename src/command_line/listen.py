import socket

# Setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('10.53.132.1', 5001))
sock.listen(1)
print("Waiting for file...")

conn, addr = sock.accept()
with open('received_file.zip', 'wb') as f:
    while True:
        data = conn.recv(4096) # Read in 4KB chunks
        if not data: break
        f.write(data)
conn.close()
print("Transfer complete.")
