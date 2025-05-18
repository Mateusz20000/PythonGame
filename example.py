import pygame
pygame.init()

screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

TILE_WIDTH = 64
TILE_HEIGHT = 32
TILEMAP_SIZE = 32

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

def screen_to_iso(mouse_x, mouse_y, camera_offset):
    mx = mouse_x - 750 - camera_offset[0]
    my = mouse_y - 100 - camera_offset[1]
    tile_x = (mx / 32 + my / 16) / 2
    tile_y = (my / 16 - mx / 32) / 2
    return int(tile_x), int(tile_y)

def draw_map(surface, camera):
    for y in range(TILEMAP_SIZE):
        for x in range(TILEMAP_SIZE):
            iso_x = (x - y) * (TILE_WIDTH // 2) + 750 + camera.offset_x
            iso_y = (x + y) * (TILE_HEIGHT // 2) + 100 + camera.offset_y
            pygame.draw.polygon(surface, (50, 150, 50), [
                (iso_x, iso_y + TILE_HEIGHT // 2),
                (iso_x + TILE_WIDTH // 2, iso_y),
                (iso_x + TILE_WIDTH, iso_y + TILE_HEIGHT // 2),
                (iso_x + TILE_WIDTH // 2, iso_y + TILE_HEIGHT)
            ], 0)

def highlight_hovered_tile(mouse_pos, camera, surface):
    tile_x, tile_y = screen_to_iso(mouse_pos[0], mouse_pos[1], (camera.offset_x, camera.offset_y))
    if 0 <= tile_x < TILEMAP_SIZE and 0 <= tile_y < TILEMAP_SIZE:
        iso_x = (tile_x - tile_y) * (TILE_WIDTH // 2) + 750 + camera.offset_x
        iso_y = (tile_x + tile_y) * (TILE_HEIGHT // 2) + 100 + camera.offset_y

        highlight = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
        highlight.fill((255, 255, 0, 80))  # semi-transparent yellow
        surface.blit(highlight, (iso_x, iso_y))

        # Show hovered coordinates
        font = pygame.font.SysFont(None, 24)
        label = font.render(f"Tile: ({tile_x}, {tile_y})", True, (255, 255, 255))
        surface.blit(label, (10, 10))

camera = Camera()

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        camera.handle_event(event)

    draw_map(screen, camera)
    mouse_pos = pygame.mouse.get_pos()
    highlight_hovered_tile(mouse_pos, camera, screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()