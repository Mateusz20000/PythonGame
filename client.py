# =============================================================
# client.py – complete working version with shop + sidebar UI
# =============================================================

import pygame
from network import Network
import library            # contains Shop, Button, Player, etc.
from library import Shop, Button, SHOP_TILES

WIDTH, HEIGHT = 1920, 1080
TILEMAP_SIZE  = 32
FPS           = 60
TILE_W, TILE_H = 64, 32         # diamond size for iso math

# ------------------------------------------------------------------
# globals the nested functions will modify
# ------------------------------------------------------------------
shop        = Shop()
shop_open   = False
buy_buttons = []
sell_buttons= []
close_btn   = None

# ------------------------------------------------------------------
# image cache so we never reload from disk twice
# ------------------------------------------------------------------
tile_images: dict[str, pygame.Surface] = {}

def get_tile_img(kind: str, stage: int):
    key = f"{kind}_{stage}"
    if key not in tile_images:
        try:
            tile_images[key] = pygame.image.load(f"tiles/{key}.png").convert_alpha()
        except FileNotFoundError:
            tile_images[key] = pygame.Surface((TILE_W, TILE_H))  # fallback
    return tile_images[key]

# ------------------------------------------------------------------
# GUI builder
# ------------------------------------------------------------------

def build_shop_gui(player):
    global buy_buttons, sell_buttons, close_btn
    font = pygame.font.SysFont(None, 26)
    buy_buttons.clear(); sell_buttons.clear()
    y0 = 180
    seeds = ["sunflower_seed", "corn_seed", "hay_seed", "pumpkin_seed"]
    crops = ["sunflower", "corn", "hay", "pumpkin"]

    for idx, seed in enumerate(seeds):
        rect = pygame.Rect(220, y0 + idx*60, 170, 40)
        buy_buttons.append(Button(rect, font,
            f"Buy {seed} ${shop.prices[seed]}",
            lambda s=seed: shop.buy_seed(player, s)))

    for idx, crop in enumerate(crops):
        rect = pygame.Rect(420, y0 + idx*60, 170, 40)
        sell_buttons.append(Button(rect, font,
            f"Sell {crop} ${shop.prices[crop]}",
            lambda c=crop: shop.sell_crop(player, c)))

    close_btn = Button(pygame.Rect(640, 130, 100, 32), font, "Close",
                       lambda: close_shop())


def close_shop():
    global shop_open
    shop_open = False

# ------------------------------------------------------------------
# Map drawing & hover detection
# ------------------------------------------------------------------

def draw_map(net: Network, surf: pygame.Surface, cam: library.Camera):
    hovered = None
    mx, my = pygame.mouse.get_pos()

    for y in range(TILEMAP_SIZE):
        for x in range(TILEMAP_SIZE):
            iso_x = (x - y) * (TILE_W//2) + 750 + cam.offset_x
            iso_y = (x + y) * (TILE_H//2) + 100 + cam.offset_y

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
                print(f"[Tile {x},{y}]", e)

            # Hover diamond hit test
            dx, dy = mx - iso_x, my - (iso_y + TILE_H//2)
            if 0 <= dx <= TILE_W and 0 <= dy <= TILE_H//2:
                if abs(dx - TILE_W//2)/(TILE_W//2) + abs(dy)/(TILE_H//2) <= 1:
                    hovered = (x, y, iso_x, iso_y)

    # highlight
    if hovered:
        x, y, ix, iy = hovered
        pts = [
            (ix+TILE_W//2, iy),
            (ix+TILE_W,     iy+TILE_H//2),
            (ix+TILE_W//2, iy+TILE_H),
            (ix,           iy+TILE_H//2)]
        pygame.draw.polygon(surf, (200,200,200), pts)
        font = pygame.font.SysFont(None, 24)
        surf.blit(font.render(f"Tile: ({x},{y})", True, (255,255,255)), (10,10))
    return hovered

# ------------------------------------------------------------------
# main game loop
# ------------------------------------------------------------------

def main():
    global shop_open
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock  = pygame.time.Clock()

    # music & networking
    music  = library.Music()
    net    = Network()
    welcome= net.stream.recv_json()
    player = library.Player.from_dict(welcome["player"])

    # camera
    cam    = library.Camera()
    selected_seed = "sunflower"

    running = True
    while running:
        screen.fill((83,219,219))

        hovered = draw_map(net, screen, cam)

        # shop popup overlay
        if shop_open:
            # dim background
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))
            panel = pygame.Surface((800, 600))
            panel.fill((230,230,230))
            screen.blit(panel, (WIDTH//2-400, HEIGHT//2-300))

            # draw buttons & handle events separately
            for btn in buy_buttons + sell_buttons:
                btn.draw(screen)
            if close_btn: close_btn.draw(screen)

            # inventory side text
            font = pygame.font.SysFont(None, 24)
            sx = WIDTH//2+200; sy = HEIGHT//2-250
            screen.blit(font.render(f"Money: ${player.money}", True, (0,0,0)), (sx, sy))
            sy += 30
            for itm, qty in player.inventory.items():
                screen.blit(font.render(f"{itm}: {qty}", True, (0,0,0)), (sx, sy)); sy += 24
        
        # ---------------- event loop ----------------------------
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

            # always handle music + camera
            cam.handle_event(ev); music.handle_event(ev)

            # toggle shop by clicking truck tiles
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and not shop_open and hovered:
                hx, hy, *_ = hovered
                if (hx, hy) in SHOP_TILES:
                    shop_open = True
                    build_shop_gui(player)
                    continue

            # when shop open – route clicks to buttons only
            if shop_open:
                for btn in buy_buttons + sell_buttons + ([close_btn] if close_btn else []):
                    btn.handle_event(ev)
                continue  # skip rest

            # ---------- gameplay hotkeys (when shop closed) -----
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1: selected_seed = "sunflower"
                elif ev.key == pygame.K_2: selected_seed = "corn"
                elif ev.key == pygame.K_3: selected_seed = "hay"
                elif ev.key == pygame.K_4: selected_seed = "pumpkin"
                elif ev.key == pygame.K_e and hovered:
                    hx, hy, *_ = hovered
                    net.harvest(hx, hy)

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and hovered:
                hx, hy, *_ = hovered
                seed_key = f"{selected_seed}_seed"
                if player.inventory.get(seed_key, 0) > 0:
                    net.plant(hx, hy, selected_seed)

        # refresh player snapshot once per frame
        snap   = net.get_player()
        player = library.Player.from_dict(snap["player"])

        # sidebar current seed
        font = pygame.font.SysFont(None, 24)
        screen.blit(font.render(f"Seed: {selected_seed}", True, (255,255,255)), (10, 30))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
