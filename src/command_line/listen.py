import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind('1.2.3.4')
sock.listen(1)
print("Waiting for file...")

conn, addr = sock.accept()
with open('received_file.zip', 'wb') as f:
    while True:
        data = conn.recv(4096) # Reads in chunks of 4KB
        if not data: break
        f.write(data)
conn.close()
print("Transfer complete.")
