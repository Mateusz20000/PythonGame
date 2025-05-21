import pygame
import sys
from library import Player

pygame.init()

# Fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("GUI Gra")
font = pygame.font.SysFont(None, 28)

# Player
player = Player(1, "Gracz", money=200)

# GUI setup
gui_panel_x = screen_width - 300
show_plants = False
show_decor = False
selected_item = None
input_quantity = ""
shopping_cart = []
message = ""

# Buttons
plants_button = pygame.Rect(gui_panel_x, 40, 200, 40)
decor_button = pygame.Rect(gui_panel_x, 90, 200, 40)
buy_button = pygame.Rect(gui_panel_x, screen_height - 60, 200, 40)

plants_panel_rect = pygame.Rect(gui_panel_x, 140, 260, 300)
decor_panel_rect = pygame.Rect(gui_panel_x, 140, 260, 160)

# Images and prices
plant_imgs = [
    ("Ground", pygame.image.load("ground.png"), 10),
    ("Sunflower", pygame.image.load("sunflower_IV.png"), 30),
    ("Pumpkin", pygame.image.load("pumpkin_VI.png"), 60),
    ("Corn", pygame.image.load("corn_IV.png"), 90),
    ("Hay", pygame.image.load("hay_V.png"), 120),
]
plant_imgs = [(name, pygame.transform.scale(img, (50, 50)), price) for name, img, price in plant_imgs]

decor_imgs = [
    ("Tree", pygame.image.load("tree_I.png"), 80),
    ("Tree II", pygame.image.load("tree_II.png"), 80)
]
decor_imgs = [(name, pygame.transform.scale(img, (50, 50)), price) for name, img, price in decor_imgs]

def draw_text(text, x, y, color=(0, 0, 0)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def calculate_total():
    return sum(item['price'] * item['quantity'] for item in shopping_cart)

clock = pygame.time.Clock()

# Main loop
while True:
    screen.fill((245, 245, 220))
    pygame.draw.rect(screen, (210, 180, 140), screen.get_rect(), 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if plants_button.collidepoint(event.pos):
                show_plants = not show_plants
                show_decor = False
                message = ""

            elif decor_button.collidepoint(event.pos):
                show_decor = not show_decor
                show_plants = False
                message = ""

            elif buy_button.collidepoint(event.pos):
                total = calculate_total()
                if total <= player.money:
                    for item in shopping_cart:
                        player.add_item(item['name'], item['quantity'])
                    player.money -= total
                    shopping_cart.clear()
                    selected_item = None
                    input_quantity = ""
                    message = "Purchase successful!"
                else:
                    message = "Not enough money!"

            elif show_plants:
                for i, (name, img, price) in enumerate(plant_imgs):
                    item_rect = pygame.Rect(plants_panel_rect.x, plants_panel_rect.y + 10 + i * 60, 260, 60)
                    if item_rect.collidepoint(event.pos):
                        selected_item = {'name': name, 'price': price}
                        input_quantity = ""
                        message = ""

            elif show_decor:
                for i, (name, img, price) in enumerate(decor_imgs):
                    item_rect = pygame.Rect(decor_panel_rect.x, decor_panel_rect.y + 10 + i * 60, 260, 60)
                    if item_rect.collidepoint(event.pos):
                        selected_item = {'name': name, 'price': price}
                        input_quantity = ""
                        message = ""

        elif event.type == pygame.KEYDOWN:
            if selected_item:
                if event.key == pygame.K_BACKSPACE:
                    input_quantity = input_quantity[:-1]
                elif event.key == pygame.K_RETURN and input_quantity.isdigit():
                    shopping_cart.append({
                        'name': selected_item['name'],
                        'quantity': int(input_quantity),
                        'price': selected_item['price']
                    })
                    input_quantity = ""
                    selected_item = None
                    message = ""
                elif event.unicode.isdigit():
                    input_quantity += event.unicode

    pygame.draw.rect(screen, (230, 230, 230), (0, 0, screen_width, 30))
    draw_text(f"Pieniądze: {player.money}", 10, 5)

    # Menu buttons
    pygame.draw.rect(screen, (230, 230, 230), plants_button)
    draw_text("Plants", plants_button.x + 10, plants_button.y + 10)
    pygame.draw.rect(screen, (230, 230, 230), decor_button)
    draw_text("Decorations", decor_button.x + 10, decor_button.y + 10)

    # Plant panel
    if show_plants:
        pygame.draw.rect(screen, (255, 255, 255), plants_panel_rect)
        for i, (name, img, price) in enumerate(plant_imgs):
            y = plants_panel_rect.y + 10 + i * 60
            screen.blit(img, (plants_panel_rect.x + 10, y))
            draw_text(f"{name} - {price}", plants_panel_rect.x + 70, y + 15)

    # Decor panel
    if show_decor:
        pygame.draw.rect(screen, (255, 255, 255), decor_panel_rect)
        for i, (name, img, price) in enumerate(decor_imgs):
            y = decor_panel_rect.y + 10 + i * 60
            screen.blit(img, (decor_panel_rect.x + 10, y))
            draw_text(f"{name} - {price}", decor_panel_rect.x + 70, y + 15)

    if selected_item:
        draw_text(f"Kupujesz: {selected_item['name']} za {selected_item['price']}", gui_panel_x, screen_height - 180)
        draw_text(f"Ilość: {input_quantity}", gui_panel_x, screen_height - 150)

    # cart
    y_cart = screen_height - 280
    for item in reversed(shopping_cart[-6:]):
        draw_text(f"{item['quantity']}x {item['name']} - {item['price'] * item['quantity']}", gui_panel_x, y_cart)
        y_cart -= 20

    draw_text(f"Summary: {calculate_total()}", gui_panel_x, screen_height - 100)
    pygame.draw.rect(screen, (230, 230, 230), buy_button)
    draw_text("Buy", buy_button.x + 70, buy_button.y + 10)

    # Equipment
    draw_text("Equipment:", 20, screen_height - 200)
    for i, (item, qty) in enumerate(player.inventory.items()):
        draw_text(f"{item}: {qty}", 20, screen_height - 180 + i * 20)

    if message:
        color = (255, 0, 0) if "Not enough money" in message else (0, 128, 0)
        draw_text(message, gui_panel_x, screen_height - 30, color)

    pygame.display.flip()
    clock.tick(30)