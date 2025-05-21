import socket, json


class LineBuffer:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buf  = b""

    def readline(self):
        line = b''
        while True:
            ch = self.sock.recv(1)
            if not ch:
                raise ConnectionError("socket closed")
            if ch == b'\n':
                break
            line += ch
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
        try: sock.connect((server, port))
        except:
            pass
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

    def get_player(self):
        return self._cmd({"op": "get_player"})

    def update_player(self, changes: dict):
        """
        changes: partial dict, e.g. {"money": 250} or
                 {"inventory": {"apple": 3, "wood": 10}}
        """
        return self._cmd({"op": "update_player", "changes": changes})
    
    def plant(self, x, y, kind):
        return self._cmd({"op": "plant", "x": x, "y": y, "kind": kind})

    def harvest(self, x, y):
        return self._cmd({"op": "harvest", "x": x, "y": y})