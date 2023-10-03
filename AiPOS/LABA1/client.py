import socket
from datetime import datetime

DEFAULT_FILENAME = "log.txt"

def write_to_file(content):
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{time_str}\t{content}\n"

    with open(DEFAULT_FILENAME, "a") as file:
        file.write(line)

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
    print("TCP DEMO CLIENT")

    current_server_addr = None
    current_port = None
    stream = None

    while True:
        buffer = input("Connect to server. Use 'connect <address> <port>' or 'quit' to exit.\n")

        if buffer.strip() == "quit":
            print("Exit...")
            if stream:
                stream.shutdown(socket.SHUT_RDWR)
            break
        elif buffer.startswith("disconnect"):
            print("You are not connected.")
        elif buffer.startswith("connect"):
            parts = buffer.split()
            if len(parts) != 3:
                print("Invalid command format. Use 'connect <address> <port>'.")
            else:
                new_server_addr = parts[1]
                new_port = parts[2]

                try:
                    new_port = int(new_port)
                except ValueError:
                    print("Invalid port format. Use 'connect <address> <port>'.")
                    continue

                current_server_addr = new_server_addr
                current_port = new_port
                print(f"Connection to {new_server_addr}:{new_port}...")

                if stream:
                    stream.shutdown(socket.SHUT_RDWR)

                try:
                    stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    stream.connect((new_server_addr, new_port))
                    print(f"Connected to {new_server_addr}:{new_port}")
                    write_to_file(f"CONNECTED to {new_server_addr}:{new_port}")
                except Exception as e:
                    print(f"Connection error: {e}")
                    stream = None
        else:
            print("You must first connect with 'connect <address> <port>'.")

        if stream:
            while True:
                buffer = input()
                if buffer.strip() == "quit":
                    print("Exit...")
                    stream.shutdown(socket.SHUT_RDWR)
                    break
                elif buffer.startswith("disconnect"):
                    print("Breaking connection...")
                    if stream:
                        stream.shutdown(socket.SHUT_RDWR)
                        stream = None
                    write_to_file(f"DISCONNECTED from {current_server_addr}:{current_port}")
                    break

                stream.send(buffer.encode('utf-8'))

                response = stream.recv(1024).decode('utf-8')
                print(f"S=>C: {response}")
                write_to_file(f"S=>C: {response}")

if __name__ == "__main__":
    main()
