import socket

def client_program():
    host = 'SERVER_IP_ADDRESS'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message = input(" -> ")
    while message.lower().strip() != 'quit':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        print(f"Received from server: {data}")
        message = input(" -> ")
    client_socket.close()

if __name__ == '__main__':
    client_program()
