
import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # print(s.sendall(b"Hello")) # None
    print(s.send(b"Hello")) # 5
    data = s.recv(1024)

print(f"received {data!r}")
