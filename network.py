# network.py
import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("192.168.0.157", 5555))
        self.buffer = ""
        self.pos = self._recvall()          # starting position from server

    def getPos(self):
        return self.pos

    def send(self, data):                   # data already like "x,y"
        self.client.sendall((data + "\n").encode())
        return self._recvall()

    # --- internal -------------------------------------------------
    def _recvall(self):
        while '\n' not in self.buffer:
            chunk = self.client.recv(2048).decode()
            if not chunk:
                raise ConnectionError("Server closed connection")
            self.buffer += chunk
        line, self.buffer = self.buffer.split('\n', 1)
        return line
