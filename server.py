import socket
from _thread import start_new_thread
import struct

server = "192.168.0.157"
port   = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(2)
print("Server started…")

def make_pos(t):
    return f"{t[0]},{t[1]}\n"

def read_pos(s):
    x, y = s.split(',')
    return int(x), int(y)

pos = [(0, 0), (100, 100)]

def threaded_client(conn, player):
    conn.sendall(make_pos(pos[player]).encode())

    buffer = ""             
    while True:
        try:
            chunk = conn.recv(2048).decode()
            if not chunk:
                break
            buffer += chunk
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                pos[player] = read_pos(line)

                other = pos[1 - player]
                conn.sendall(make_pos(other).encode())
        except OSError:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1