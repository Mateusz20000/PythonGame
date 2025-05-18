import socket, json


class LineBuffer:
    """Read / write  '\n'-terminated lines on a blocking socket."""
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buf  = b""

    def readline(self) -> bytes:
        while b"\n" not in self.buf:
            try:
                chunk = self.sock.recv(1024)
                if not chunk:
                    raise ConnectionError("socket closed")
                self.buf += chunk
            except ConnectionResetError:
                raise ConnectionError("connection reset by peer")
        line, self.buf = self.buf.split(b"\n", 1)
        return line

    def sendline(self, data: bytes | str):
        if isinstance(data, str):
            data = data.encode()
        self.sock.sendall(data + b"\n")

    def recv_json(self):
        return json.loads(self.readline().decode())

    def send_json(self, obj):
        self.sendline(json.dumps(obj).encode())

    def close(self):
        self.sock.close()



class Network:
    def __init__(self, server="192.168.0.157", port=5555):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))
        self.stream = LineBuffer(sock)

    def send(self, text_line: str) -> str:
        self.stream.sendline(text_line)
        return self.stream.readline().decode()

    def _cmd(self, obj: dict) -> dict:
        self.stream.send_json(obj)
        return self.stream.recv_json()

    def ping(self):
        return self._cmd({"op": "ping"})

    def get_tile(self, x: int, y: int):
        return self._cmd({"op": "get", "x": x, "y": y})

    def set_tile(self, x: int, y: int, tile: dict):
        return self._cmd({"op": "set", "x": x, "y": y, "tile": tile})

    def close(self):
        self.stream.close()