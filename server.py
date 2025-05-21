import socket
import threading
import json
import library
import network
import time
import random


class TileServer:

    def __init__(self, host="192.168.0.157", port=5555, size=(23, 23)):

        default_tile = library.Tile("grass")
        self.map = library.TileMap(size[0], size[1], default_tile)
        #b1 = library.Tile("truck_front", None)
        #b2 = library.Tile("truck_back", None)
        #self.map.set(5, 6, b1)
        #self.map.set(5, 5, b2)
        self.host = host
        self.port = port
        self.players  = {}
        self.next_pid = 1
        threading.Thread(target=self._growth_loop, daemon=True).start()

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
                #self.players[pid] = library.Player()
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
                t = self.map.get(x, y)
                return {"ok": True, "tile": t.to_dict()}

            elif op == "set":

                x, y = request["x"], request["y"]
                t_data = request["tile"]
                new_tile = library.Tile.from_dict(t_data)
                self.map.set(x, y, new_tile)


                return {"ok": True}
            
            if op == "get_player":
                return {"ok": True, "player": self.players[pid].to_dict()}

            if op == "update_player":
                changes = request["changes"]
                p = self.players[pid]
                if "money" in changes:
                    p.money = changes["money"]
                if "inventory" in changes:
                    p.inventory = changes["inventory"]
                    return {"ok": True}
                
            if op == "plant":
                x, y, kind = request["x"], request["y"], request["kind"].lower()
                tile = self.map.get(x, y)
                plant   = self.players[pid]

                seed_key = f"{kind}_seed"
                if tile.plant or plant.inventory.get(seed_key, 0) <= 0:
                    return {"ok": False, "err": "cant_plant"}
                plant.inventory[seed_key] -= 1
                tile.plant = library.Plant(kind, 1)
                return {"ok": True}
            
            elif op == "harvest":
                x, y = request["x"], request["y"]
                tile = self.map.get(x, y)
                player = self.players[pid]

                if tile.plant and tile.plant.is_mature():
                    prod_key = tile.plant.kind
                    tile.plant = None
                    player.add_item(prod_key, 1)
                    return {"ok": True}

                return {"ok": False, "err": "not_mature"}

            else:

                return {"ok": False, "error": f"Unknown op: {op}"}
            
        except Exception as e:

            return {"ok": False, "error": str(e)}
        
    def _growth_loop(self):
        while True:
            time.sleep(10)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    t = self.map.get(x, y)
                    if t.plant:
                        
                        ran = random.randint(0,2)
                        if ran == 1:
                            t.plant.grow()
        



server = TileServer()
server.start()
