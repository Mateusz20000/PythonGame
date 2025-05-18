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


def show(n, s, size):

        grass_img = pygame.image.load("tiles/grass.png").convert_alpha()

        for y in range(size):
            for x in range(size):
                iso_x = (x - y) * (64 // 2) + 750
                iso_y = (x + y) * (32 // 2) + 100

                try:
                    response = n.get_tile(x,y)
                    tiled = response["tile"]["terrain"]
                    if(tiled == "grass"):
                        s.blit(grass_img, (iso_x, iso_y))
                except ConnectionError:
                    print("Server closed the connection.")
                    return

                #if(tile_type["terrain"] == "grass"):
                #    s.blit(pygame.image.load("tiles\grass.png").convert_alpha(), (iso_x, iso_y))

                #s.blit(n.get_tile(x, y), (iso_x, iso_y))

        pygame.display.update()


                



def main():

    run = True
    clock = pygame.time.Clock()
    network = Network()
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))

#    print(n.ping())                     # {'ok': True, 'msg': 'pong'}

#    print(n.get_tile(4, 7))             # {'ok': True, 'tile': {...}}

#    n.set_tile(4, 7,
#        {"terrain": "soil",
#        "plant":   {"kind": "carrot", "stage": 0}})






    while run:

        clock.tick(60)

        show(network, screen, 32)

        #try:
        #    print(network.get_tile(0,0))
        #except ConnectionError:
        #    print("Server closed the connection.")
        #    return




        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False
                pygame.quit()





main()