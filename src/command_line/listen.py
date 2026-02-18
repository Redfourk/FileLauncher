import socket

# Setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 5001))
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
