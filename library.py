import pygame
import random
import plants
import threading




class Player:

    def __init__(self, pid, name = "guest", money=0, inventory=None):
        self.id = pid
        self.name = name
        self.money = money
        self.inventory = inventory or {}

        self.add_item("sunflower_seed", 10)
        self.add_item("hay_seed", 10)
        self.add_item("corn_seed", 10)
        self.add_item("pumpkin_seed", 10)

    def to_dict(self):
        return {
            "id":        self.id,
            "name":      self.name,
            "money":     self.money,
            "inventory": self.inventory,
        }

    @staticmethod
    def from_dict(d):
        return Player(
            d["id"],
            d["name"],
            d.get("money", 0),
            d.get("inventory", {}),
        )

    def add_money(self, amount):
        self.money += amount

    def add_item(self, item, qty=1):
        self.inventory[item] = self.inventory.get(item, 0) + qty



PLANT_STAGES = {"corn": 4, "hay": 5, "sunflower": 4, "pumpkin": 6}


class Plant:
    def __init__(self, kind: str, stage: int = 1):
        self.kind  = kind.lower()
        self.stage = stage
        self.max_stage = PLANT_STAGES[self.kind]

    def grow(self):
        if self.stage < self.max_stage:
            self.stage += 1

    def is_mature(self) -> bool:
        return self.stage >= self.max_stage

    def to_dict(self):
        return {"kind": self.kind, "stage": self.stage}

    @staticmethod
    def from_dict(d):
        return Plant(d["kind"], d["stage"])



class Tile:
    def __init__(self, terrain="grass", plant: Plant | None = None):
        self.terrain = terrain
        self.plant   = plant

    def to_dict(self):
        return {
            "terrain": self.terrain,
            "plant": self.plant.to_dict() if self.plant else None
        }

    @staticmethod
    def from_dict(d):
        p = d.get("plant")
        return Tile(d["terrain"], Plant.from_dict(p) if p else None)



class TileMap:
    """
    stores a real 2-D grid:  tiles[y][x]  (row-major)
    every cell holds its *own* Tile instance
    """
    def __init__(self, width, height, default_tile: Tile):
        self.width  = width
        self.height = height

        self.tiles = [
            [Tile(default_tile.terrain,
                  None if default_tile.plant is None
                  else Plant(default_tile.plant.kind, default_tile.plant.stage))
             for _ in range(width)]
            for _ in range(height)
        ]
        self.lock = threading.Lock()

    def _check(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Invalid position ({x},{y})")

    def get(self, x, y):
        self._check(x, y)
        with self.lock:
            return self.tiles[y][x]

    def set(self, x, y, tile: Tile):
        self._check(x, y)
        with self.lock:
            self.tiles[y][x] = tile





class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.last_mouse_pos = (0, 0)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.dragging = True
            self.last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = pygame.mouse.get_pos()
            dx = mx - self.last_mouse_pos[0]
            dy = my - self.last_mouse_pos[1]
            self.offset_x += dx
            self.offset_y += dy
            self.last_mouse_pos = (mx, my)





MUSIC_END = pygame.USEREVENT + 1

class Music:

    def __init__(self):

        pygame.mixer.init()

        self.playlist = [
            "bgplaylist/Wake-up.ogg",
            "bgplaylist/The-Farmer.ogg",
            "bgplaylist/Happy-Farm.ogg",
            "bgplaylist/The-Farmer.ogg",
        ]

        self.current = 0

        MUSIC_END = pygame.USEREVENT + 1

        pygame.mixer.music.set_endevent(MUSIC_END)

        self.play_next()

    def play_next(self):
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play()
        self.current = (self.current + 1) % len(self.playlist)
    def handle_event(self, event):
        if event.type == MUSIC_END:
            self.play_next()

