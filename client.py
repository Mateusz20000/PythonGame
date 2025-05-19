import pygame
from network import Network
import tile

#width = 500
#height = 500

#win = pygame.display.set_mode((width, height))
#pygame.display.set_caption("Client")

#clientNumber = 0

#class Player():

#    def __init__(self, x, y, width, height, color):
#        self.x = x
#        self.y = y
#        self.width = width
#        self.height = height
#        self.color = color
#        self.rect = (x,y,width,height)
#        self.vel = 3

#    def draw(self, win):
#        pygame.draw.rect(win, self.color, self.rect)

#    def move(self):
#        keys = pygame.key.get_pressed()

#        if keys[pygame.K_LEFT]:
#            self.x -= self.vel

#        if keys[pygame.K_RIGHT]:
#            self.x += self.vel

#        if keys[pygame.K_UP]:
#            self.y -= self.vel

#        if keys[pygame.K_DOWN]:
#            self.y += self.vel

#        self.update()

#    def update(self):
#        self.rect = (self.x, self.y, self.width, self.height)
        

#def read_pos(s):
#    x, y = s.split(",")
#    return int(x), int(y)


#def make_pos(tup):
#    return str(tup[0]) + "," + str(tup[1])



#    pygame.display.update()



def show(n, s, camera, tile_images, size):
    hovered_tile = None
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for y in range(size):
        for x in range(size):
            iso_x = (x - y) * 32 + 750 + camera.offset_x
            iso_y = (x + y) * 16 + 100 + camera.offset_y

            try:
                response = n.get_tile(x, y)
                terrain = response["tile"]["terrain"]
                image = tile_images.get(terrain)

                if image:
                    s.blit(image, (iso_x, iso_y))
            except Exception as e:
                print(f"[Error fetching tile {x},{y}]: {e}")

            # Check for hover
            rel_x = mouse_x - iso_x
            rel_y = mouse_y - iso_y - 32

            # Diamond hitbox
            if 0 <= rel_x <= 64 and 0 <= rel_y <= 32:
                # Diamond equation
                dx = abs(rel_x - 32)
                dy = abs(rel_y - 16)
                if dx / 32 + dy / 16 <= 1:
                    hovered_tile = (x, y, iso_x, iso_y)

    # Draw hover highlight AFTER terrain tiles
    if hovered_tile:
        x, y, iso_x, iso_y = hovered_tile

        # Create a diamond shape highlight
        points = [
            (iso_x + 32, iso_y + 32),       # top #I ADDED IT HERE
            (iso_x + 64, iso_y + 48),  # right
            (iso_x + 32, iso_y + 64),  # bottom
            (iso_x, iso_y + 48),       # left
        ]
        pygame.draw.polygon(s, (255, 255, 0, 80), points)

        # Coordinates overlay
        font = pygame.font.SysFont(None, 24)
        label = font.render(f"Tile: ({x}, {y})", True, (255, 255, 255))
        s.blit(label, (10, 10))

        #changing for flowwers
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                s1 = tile.Tile("sunflower",None)

                n.set_tile(x, y, s1)



        


def screen_to_iso_tile(mx, my, camera_offset_x, camera_offset_y):
    # Adjust for camera and origin offset
    mx -= (750 + camera_offset_x)
    my -= (100 + camera_offset_y)

    # Inverse of isometric transform
    x = (mx / 32 + my / 16) / 2
    y = (my / 16 - mx / 32) / 2

    return int(x), int(y)


def main():

    run = True
    clock = pygame.time.Clock()
    network = Network()
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    camera = tile.Camera()

    tile_images = {
        "grass": pygame.image.load("tiles/grass.png").convert_alpha(),
        "sunflower": pygame.image.load("tiles/sunflower_IV.png").convert_alpha(),
        "truck_front": pygame.image.load("tiles/truck_front.png").convert_alpha(),
        "truck_back": pygame.image.load("tiles/truck_back.png").convert_alpha()
    }

#    print(n.ping())                     # {'ok': True, 'msg': 'pong'}

#    print(n.get_tile(4, 7))             # {'ok': True, 'tile': {...}}

#    n.set_tile(4, 7,
#        {"terrain": "soil",
#        "plant":   {"kind": "carrot", "stage": 0}})






    while run:

        clock.tick(60)

        screen.fill((83, 219, 219))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False
                

            camera.handle_event(event)


    

        show(network, screen, camera, tile_images, 32)

        pygame.display.update()

    pygame.quit()





main()
