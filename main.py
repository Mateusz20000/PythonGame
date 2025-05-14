import pygame
import pytmx

def grid_to_iso(x, y, tile_width, tile_height):
    screen_x = (x - y) * (tile_width // 2)
    screen_y = (x + y) * (tile_height // 2)
    return screen_x, screen_y

# Init
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

# Example tile size
#TILE_WIDTH = 64
#TILE_HEIGHT = 32

# Example isometric tiles (replace with real images)
#tile_img = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
#pygame.draw.polygon(tile_img, (100, 200, 100), [(32,0), (64,16), (32,32), (0,16)])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    tmx_data = pytmx.util_pygame.load_pygame("map.tmx")

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen_x, screen_y = (x - y) * 32 + 900, (x + y) * 16 + 250
                    screen.blit(tile, (screen_x, screen_y))

    #for x in range(10):
    #    for y in range(10):
    #        iso_x, iso_y = grid_to_iso(x, y, TILE_WIDTH, TILE_HEIGHT)
    #        screen.blit(tile_img, (iso_x + 400, iso_y + 100))  # +offset

    pygame.display.flip()
    clock.tick(60)


pygame.quit()