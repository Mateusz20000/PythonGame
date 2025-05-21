import pygame
from network import Network
import library

WIDTH, HEIGHT = 1920, 1080
TILEMAP_SIZE = 23
FPS = 60


tile_images: dict[str, pygame.Surface] = {}
def get_tile_img(kind: str, stage: int):
    key = f"{kind}_{stage}"
    if key not in tile_images:
        tile_images[key] = pygame.image.load(
            f"tiles/{kind}_{stage}.png").convert_alpha()
    return tile_images[key]

def draw_map(net: Network, surf: pygame.Surface, cam: library.Camera, hovered, size=TILEMAP_SIZE):
    hovered_tile = None
    mx, my = pygame.mouse.get_pos()

    for y in range(size):
        for x in range(size):
            iso_x = (x - y) * 32 + 750 + cam.offset_x
            iso_y = (x + y) * 16 + 100 + cam.offset_y

            try:
                r = net.get_tile(x, y)
                terrain = r["tile"]["terrain"]
                plant   = r["tile"]["plant"]
                if plant:
                    img = get_tile_img(plant["kind"], plant["stage"])
                else:
                    img = get_tile_img(terrain, 0)
                surf.blit(img, (iso_x, iso_y))
            except Exception as e:
                print(f"[Tile {x},{y}] {e}")

            # diamond hit-test
            dx, dy = mx - iso_x, my - (iso_y + 32)
            if 0 <= dx <= 64 and 0 <= dy <= 32:
                if abs(dx - 32) / 32 + abs(dy - 16) / 16 <= 1:
                    hovered_tile = (x, y, iso_x, iso_y)

    if hovered_tile:
        x, y, ix, iy = hovered_tile
        pts = [(ix+32, iy+32), (ix+64, iy+48), (ix+32, iy+64), (ix, iy+48)]
        pygame.draw.polygon(surf, (200, 200, 200), pts, 0)
        font = pygame.font.SysFont(None, 24)
        surf.blit(font.render(f"Tile: ({x},{y})", True, (255,255,255)), (10, 10))

    return hovered_tile

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock  = pygame.time.Clock()

    music = library.Music()

    net = Network()
    try:
        welcome = net.stream.recv_json()
    except ConnectionError as e:
        print(f"Connection failed: {e}")
        return
    player  = library.Player.from_dict(welcome["player"])
    player.add_item("hay_seed", 10)

    camera = library.Camera()

    selected_seed = "sunflower"
    running = True


    while running:
        screen.fill((83, 219, 219))

        hovered = draw_map(net, screen, camera, None)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            camera.handle_event(ev)
            music.handle_event(ev)

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1: selected_seed = "sunflower"
                elif ev.key == pygame.K_2: selected_seed = "corn"
                elif ev.key == pygame.K_3: selected_seed = "hay"
                elif ev.key == pygame.K_4: selected_seed = "pumpkin"
                elif ev.key == pygame.K_e and hovered:
                    x, y, *_ = hovered
                    net.harvest(x, y)

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and hovered:
                x, y, *_ = hovered
                seed_key = f"{selected_seed}_seed"
                if player.inventory.get(seed_key, 0) > 0:
                    net.plant(x, y, selected_seed)
            
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_e and hovered:
                x, y, *_ = hovered
                net.harvest(x, y)     

        snap   = net.get_player()
        player = library.Player.from_dict(snap["player"])

        font = pygame.font.SysFont(None, 24)
        screen.blit(
            font.render(f"Selected: {selected_seed}", True, (255,255,255)),
            (10, 30)
        )

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


main()
