import socket
import rabin

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 12345)
server_socket.bind(server_address)

server_socket.listen(5)
print("The server is listening on {}:{}".format(*server_address))

while True:
    client_socket, client_address = server_socket.accept()
    print("Connection from:", client_address)

    data = client_socket.recv(1024)

    if data:
        response = f"result of verification: {rabin.V(*data.decode('utf-8').split(','))}"
        client_socket.send(response.encode('utf-8'))

    client_socket.close()
