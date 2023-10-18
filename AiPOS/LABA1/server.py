import socket

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

while True:
    server_socket.listen(1)

    print(f"Server listening on {HOST}:{PORT}")
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        received_data = data.decode()
        print(f"Received: {received_data}")

        if ".." in received_data:
            response = "The session has ended."
            client_socket.send(response.encode())
            break

        words = received_data.strip(".").split()
        reversed_sentence = " ".join(reversed(words))
        client_socket.send(reversed_sentence.encode())

    client_socket.close()
    server_socket.close()
