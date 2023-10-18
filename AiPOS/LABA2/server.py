import socket

HOST = '127.0.0.1'
PORT = 12346

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Server listening on {HOST}:{PORT}")

while True:
    data, client_address = server_socket.recvfrom(1024)

    if not data:
        continue

    received_data = data.decode()
    print(f"Received: {received_data}")

    if ".." in received_data:
        response = "The session has ended."
        server_socket.close()
        break
    else:
        words = received_data.strip(".").split()
        reversed_sentence = " ".join(reversed(words))
        response = reversed_sentence

    server_socket.sendto(response.encode(), client_address)
