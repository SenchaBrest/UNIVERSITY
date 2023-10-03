import socket
import threading

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)
        if not request:
            break

        input_str = request.decode('utf-8')

        if ".." in input_str:
            client_socket.send(b"Breaking connection...\n")
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
            break
        elif "." in input_str:
            words = input_str.split()
            reversed_words = list(reversed(words))
            reversed_str = ' '.join(reversed_words)
            client_socket.send(reversed_str.encode('utf-8'))
        else:
            client_socket.send(input_str.encode('utf-8'))

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 6666))
    server.listen(5)

    print("TCP SERVER DEMO - Listening on port 6666")

    while True:
        client_socket, addr = server.accept()
        print("New connection from:", addr)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
