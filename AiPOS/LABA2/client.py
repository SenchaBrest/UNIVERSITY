import socket
from datetime import datetime

DEFAULT_FILENAME = "log.txt"

def write_to_file(content):
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{time_str}\t{content}\n"

    with open(DEFAULT_FILENAME, "a") as file:
        file.write(line)

def main():
    print("UDP DEMO CLIENT")

    current_server_addr = None
    current_port = None
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        buffer = input("Connect to server. Use 'connect <address> <port>' or 'quit' to exit.\n")

        if buffer.strip() == "quit":
            print("Exit...")
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

        else:
            print("You must first connect with 'connect <address> <port>'.")
            continue

        while True:
            buffer = input()
            if buffer.strip() == "quit":
                print("Exit...")
                break
            elif buffer.startswith("disconnect"):
                print("Breaking connection...")
                current_server_addr = None
                current_port = None
                break

            client_socket.sendto(buffer.encode('utf-8'), (current_server_addr, current_port))
            response, _ = client_socket.recvfrom(1024)
            response_str = response.decode('utf-8')
            print(f"S=>C: {response_str}")
            write_to_file(f"S=>C: {response_str}")

if __name__ == "__main__":
    main()
