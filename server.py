import socket
import threading
import json
import library
import network



class TileServer:

    def __init__(self, host="192.168.0.157", port=5555, size=(32, 32)):

        default_tile = library.Tile("grass")
        self.map = library.TileMap(size[0], size[1], default_tile)
        b1 = library.Tile("truck_front", None)
        b2 = library.Tile("truck_back", None)
        self.map.set(5, 6, b1)
        self.map.set(5, 5, b2)
        self.host = host
        self.port = port
        self.players  = {}
        self.next_pid = 1

    def start(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f"[Server] Listening on {self.host}:{self.port}")

            while True:

                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):

        print(f"[Connect] {addr}")

        try:

            with conn, conn.makefile("rwb") as f:

                pid = self.next_pid; self.next_pid += 1
                self.players[pid] = library.Player(pid, f"Player{pid}", money=100)
                stream = network.LineBuffer(conn)
                stream.send_json({"op": "welcome", "player": self.players[pid].to_dict()})

                while True:

                    line = f.readline()

                    if not line:

                        break

                    request = json.loads(line.decode())
                    response = self.handle_request(request, pid)
                    f.write(json.dumps(response).encode() + b"\n")
                    f.flush()

        except Exception as e:

            print(f"[Error] {addr}: {e}")

        finally:

            print(f"[Disconnect] {addr}")


    def handle_request(self, request, pid):

        op = request.get("op")

        try:

            if op == "ping":

                return {"ok": True, "msg": "pong"}

            elif op == "get":

                x, y = request["x"], request["y"]
                t = self.map.get(x, y)                     # t is a Tile
                return {"ok": True, "tile": t.to_dict()}   # ← fixed name

            elif op == "set":

                x, y = request["x"], request["y"]
                t_data = request["tile"]
                new_tile = library.Tile.from_dict(t_data)   # ← no shadowing
                self.map.set(x, y, new_tile)

                if t_data == "sunflower":
                    self.players[pid].add_item("sunflower", -1)

                return {"ok": True}
            
            if op == "get_player":
                return {"ok": True, "player": self.players[pid].to_dict()}

            if op == "update_player":
                changes = request["changes"]           # e.g. {"money": 150}
                p = self.players[pid]
                if "money" in changes:
                    p.money = changes["money"]
                if "inventory" in changes:
                    p.inventory = changes["inventory"]
                    return {"ok": True}

            else:

                return {"ok": False, "error": f"Unknown op: {op}"}
            
        except Exception as e:

            return {"ok": False, "error": str(e)}
        



server = TileServer()
server.start()





#server = "192.168.0.157"
#port   = 5555

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((server, port))
#s.listen(2)
#print("Server started…")

#def make_pos(t):
#    return f"{t[0]},{t[1]}\n"

#def read_pos(s):
#    x, y = s.split(',')
#    return int(x), int(y)

#pos = [(0, 0), (100, 100)]

#def threaded_client(conn, player):
#    conn.sendall(make_pos(pos[player]).encode())

#    buffer = ""             
#    while True:
#        try:
#            chunk = conn.recv(2048).decode()
#            if not chunk:
#                break
#            buffer += chunk
#            while '\n' in buffer:
#                line, buffer = buffer.split('\n', 1)
#                pos[player] = read_pos(line)

#                other = pos[1 - player]
#                conn.sendall(make_pos(other).encode())
#        except OSError:
#            break

#    print("Lost connection")
#    conn.close()

#currentPlayer = 0
#while True:
#    conn, addr = s.accept()
#    start_new_thread(threaded_client, (conn, currentPlayer))
#    currentPlayer += 1