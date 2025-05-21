import pygame
import random
import plants 
import threading


class Player:

    def __init__(self, pid, name, money=0, inventory=None):
        self.id        = pid
        self.name      = name
        self.money     = money
        self.inventory = inventory or {}

        self.add_item("sunflower", 10)

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


class Plant:
    def __init__(self, kind, stage=0):
        self.kind = kind
        self.stage = stage

    def to_dict(self):
        return {"kind": self.kind, "stage": self.stage}

    @staticmethod
    def from_dict(data):
        return Plant(data["kind"], data.get("stage", 0))


class Tile:
    def __init__(self, terrain, plant=None):
        self.terrain = terrain
        self.plant = plant

    def to_dict(self):
        return {
            "terrain": self.terrain,
            "plant": self.plant.to_dict() if self.plant else None
        }

    @staticmethod                       # needed so we can call Tile.from_dict(...)
    def from_dict(data):
        p = data.get("plant")
        plant = None if p is None else Plant.from_dict(p)
        return Tile(data["terrain"], plant)


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


