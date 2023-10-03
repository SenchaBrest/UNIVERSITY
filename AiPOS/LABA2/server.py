import socket

def handle_client(data, client_address, server_socket):
    input_str = data.decode('utf-8')

    if ".." in input_str:
        server_socket.sendto(b"Breaking connection...\n", client_address)
    elif "." in input_str:
        words = input_str.split()
        reversed_words = list(reversed(words))
        reversed_str = ' '.join(reversed_words)
        server_socket.sendto(reversed_str.encode('utf-8'), client_address)
    else:
        server_socket.sendto(input_str.encode('utf-8'), client_address)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 6666))

    print("UDP SERVER DEMO - Listening on port 6666")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        print("Received data from:", client_address)
        handle_client(data, client_address, server_socket)

if __name__ == "__main__":
    main()
