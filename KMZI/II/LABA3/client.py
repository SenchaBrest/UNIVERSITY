import socket
import rabin

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 12345)
client_socket.connect(server_address)

rabin.G("01")

message = "00112233445566778899aabbccddeeff"
sig, pad = rabin.S(message)
print(sig, pad)
message = f'{message},{pad},{sig[2:]}'
client_socket.send(message.encode('utf-8'))

data = client_socket.recv(1024)
print("Response from the server:", data.decode('utf-8'))

client_socket.close()
