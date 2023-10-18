import socket
import threading
import datetime
import readchar


def receive_messages(client_socket):
    while True:
        data, server_address = client_socket.recvfrom(1024)
        if not data:
            with open("log.txt", "a") as log:
                log.write(
                    f"Disconnecting from the current server..."
                    f"\tDisconnected at: {datetime.datetime.now()}\n")
            print("DISCONNECTED")
            break
        message = data.decode('utf-8')
        print(f"Received from server: {message}")
        log_message = f"Received from server: {message}" \
                      f"\tReceived at: {datetime.datetime.now()}"
        with open("log.txt", "a") as log:
            log.write(log_message + "\n")


def connect_to_server(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((server_host, server_port))
    log_message = f"Connected to server at {server_host}:{server_port}" \
                  f"\tConnected at: {datetime.datetime.now()}"
    print("CONNECTED")
    with open("log.txt", "a") as log:
        log.write(log_message + "\n")

    return client_socket


def custom_input():
    input_text = ""
    while True:
        char = readchar.readchar()
        if char == readchar.key.ENTER:  # Enter key
            break
        elif char == "@":  # @ key
            break
        elif char == readchar.key.CTRL_C:  # Handle Ctrl+C as an interruption
            raise KeyboardInterrupt
        elif char == readchar.key.CTRL_D:  # Handle Ctrl+D as an EOF
            raise EOFError
        else:
            input_text += char
            print(char, end='', flush=True)

    print("")
    return input_text


def main():
    client_socket = None

    server_host, server_port = None, None
    while True:
        user_input = custom_input()

        if user_input.startswith("connect"):
            _, server_host, server_port = user_input.split()
            server_port = int(server_port)
            if client_socket:
                with open("log.txt", "a") as log:
                    log.write(
                        f"Disconnecting from the current server..."
                        f"\tDisconnected at: {datetime.datetime.now()}\n")
                print("DISCONNECTED")
                client_socket.close()
            client_socket = connect_to_server(server_host, server_port)
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.start()

        elif user_input.startswith("disconnect"):
            if client_socket:
                with open("log.txt", "a") as log:
                    log.write(
                        f"Disconnecting from the current server..."
                        f"\tDisconnected at: {datetime.datetime.now()}\n")
                print("DISCONNECTED")
                client_socket.close()
                client_socket = None
            else:
                print("Not currently connected to a server.")

        elif client_socket:
            server_address = (server_host, server_port)
            client_socket.sendto(user_input.encode('utf-8'), server_address)


if __name__ == "__main__":
    main()
