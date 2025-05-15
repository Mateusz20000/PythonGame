import pygame
import pytmx

def grid_to_iso(x, y, tile_width, tile_height):
    screen_x = (x - y) * (tile_width // 2)
    screen_y = (x + y) * (tile_height // 2)
    return screen_x, screen_y

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

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
                    screen_x, screen_y = (x - y) * 16 + 900, (x + y) * 8 + 250
                    screen.blit(tile, (screen_x, screen_y))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
