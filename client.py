import pygame
from network import Network
import library


def show(network, surface, camera, tile_images, player, size):
    hovered_tile = None
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for y in range(size):
        for x in range(size):
            iso_x = (x - y) * 32 + 750 + camera.offset_x
            iso_y = (x + y) * 16 + 100 + camera.offset_y

            try:
                response = network.get_tile(x, y)
                terrain = response["tile"]["terrain"]
                image = tile_images.get(terrain)

                if image:
                    surface.blit(image, (iso_x, iso_y))
            except Exception as e:
                print(f"[Error fetching tile {x},{y}]: {e}")

            rel_x = mouse_x - iso_x
            rel_y = mouse_y - iso_y - 32

            if 0 <= rel_x <= 64 and 0 <= rel_y <= 32:
                dx = abs(rel_x - 32)
                dy = abs(rel_y - 16)
                if dx / 32 + dy / 16 <= 1:
                    hovered_tile = (x, y, iso_x, iso_y)

    if hovered_tile:
        x, y, iso_x, iso_y = hovered_tile

        points = [
            (iso_x + 32, iso_y + 32),
            (iso_x + 64, iso_y + 48),
            (iso_x + 32, iso_y + 64),
            (iso_x, iso_y + 48)
        ]
        pygame.draw.polygon(surface, (200, 200, 200), points)

        font = pygame.font.SysFont(None, 24)
        label = font.render(f"Tile: ({x}, {y})", True, (255, 255, 255))
        surface.blit(label, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and player.inventory["sunflower"] > 0:

                s1 = library.Tile("sunflower",None).to_dict()

                network.set_tile(x, y, s1)




        


def screen_to_iso_tile(mx, my, camera_offset_x, camera_offset_y):
    mx -= (750 + camera_offset_x)
    my -= (100 + camera_offset_y)

    x = (mx / 32 + my / 16) / 2
    y = (my / 16 - mx / 32) / 2

    return int(x), int(y)


def main():

    run = True
    clock = pygame.time.Clock()
    network = Network()
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    camera = library.Camera()

    welcome = network.stream.recv_json()
    player = library.Player.from_dict(welcome["player"])
    

    tile_images = {
        "grass": pygame.image.load("tiles/grass.png").convert_alpha(),
        "sunflower": pygame.image.load("tiles/sunflower_IV.png").convert_alpha(),
        "truck_front": pygame.image.load("tiles/truck_front.png").convert_alpha(),
        "truck_back": pygame.image.load("tiles/truck_back.png").convert_alpha()
    }



    while run:

        clock.tick(60)

        screen.fill((83, 219, 219))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False
                

            camera.handle_event(event)




        show(network, screen, camera, tile_images, player, 32)



        nfplayer = network.get_player()
        player = library.Player.from_dict(nfplayer["player"])

        pygame.display.update()

    pygame.quit()





main()
