import pygame
import random
import plants
import threading

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
    def __init__(self, terrain="grass", plant=None):
        self.terrain = terrain          # e.g. 'grass', 'soil'
        self.plant   = plant            # Plant | None

    # ✨ CORRECT NAME  (was to_dictt)
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
        # copy the default tile into every position so they are independent
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






#tile_width = 64
#tile_height = 32

#size = 20


#def show(screen, grid, size):
#        for y in range(size):
#            for x in range(size):
#                iso_x = (x - y) * (tile_width // 2) + 750
#                iso_y = (x + y) * (tile_height // 2) + 100
#
#                screen.blit(grid[y][x].plant.show(), (iso_x, iso_y))


    
#def main():

    #pygame.init()
    #screen = pygame.display.set_mode((1920, 1080))
    #clock = pygame.time.Clock()



    #grid = [[Tile(plants.Pumpkin()) for x in range(size)] for y in range(size)]




    

    #pygame.display.flip()
    #status = True
    #while (status):

    #    for event in pygame.event.get():

    #        if event.type == pygame.QUIT:
    #            status = False


    #    for y in range(size):
    #        for x in range(size):
                
    #            ran = random.randint(0,250)
    #            if ran == 10:
    #                grid[y][x].plant.grow()

    #    show(screen, grid, size)


    #    pygame.display.flip()
    #    clock.tick(60)

    #pygame.quit()


#main()