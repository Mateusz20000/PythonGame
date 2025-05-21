import pygame
import random
import plants
import threading
import time



PLANT_STAGES = {"corn": 4, "hay": 5, "sunflower": 4, "pumpkin": 6}
MUSIC_END = pygame.USEREVENT + 1
SHOP_TILES = {(5, 5), (5, 6)}

class Player:

    def __init__(self, pid, name = "guest", money=0, inventory=None):
        self.id = pid
        self.name = name
        self.money = money
        self.inventory = inventory or {}

        self.add_item("sunflower_seed", 30)
        self.add_item("hay_seed", 30)
        self.add_item("corn_seed", 30)
        self.add_item("pumpkin_seed", 30)

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
        pygame.mixer.music.set_volume(0.06)
        pygame.mixer.music.play()
        self.current = (self.current + 1) % len(self.playlist)
    def handle_event(self, event):
        if event.type == MUSIC_END:
            self.play_next()



class Button:
    """Clickable rectangle that re‑renders its label on demand."""
    def __init__(self, rect: pygame.Rect, font: pygame.font.Font, text: str, callback):
        self.rect = rect
        self.font = font
        self.text = text
        self.callback = callback
        self._render()

    def _render(self):
        self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

    def set_text(self, new_text: str):
        self.text = new_text
        self._render()

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, (200, 200, 200), self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        tx = self.rect.x + (self.rect.w - self.txt_surface.get_width()) // 2
        ty = self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2
        surf.blit(self.txt_surface, (tx, ty))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos):
            self.callback()
            


class Shop:
    BASE = {
        "corn": 10, "hay": 5, "sunflower": 15, "pumpkin": 20,
        "corn_seed": 3, "hay_seed": 2, "sunflower_seed": 5, "pumpkin_seed": 8,
    }

    def __init__(self):
        self.prices = self.BASE.copy()
        threading.Thread(target=self._price_loop, daemon=True).start()

    def _price_loop(self):
        while True:
            time.sleep(random.randint(20, 40))
            self.update_prices()

    def update_prices(self):
        for k in self.prices:
            change = random.uniform(-0.2, 0.2)
            self.prices[k] = max(1, int(self.prices[k] * (1 + change)))
    
    def buy_seed(self, player, seed):
        p = self.prices[seed]
        if player.money >= p:
            player.money -= p
            player.add_item(seed, 1)
            return True
        return False

    def sell_crop(self, player, crop):
        if player.inventory.get(crop, 0) > 0:
            player.inventory[crop] -= 1
            player.money += self.prices[crop]
            return True
        return False