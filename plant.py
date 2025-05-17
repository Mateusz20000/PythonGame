import pygame
import random

class Sunflower:

    def __init__(self):
        self.state = 1
        self.name = "sunflower"

    def grow(self):
        
        if self.state < 4:
            self.state += 1

    
class Tile:

    def show(self, Plant):

        if Plant.name == "sunflower" :
            if Plant.state == 1:
                return pygame.image.load("tiles\sunflower_I.png").convert()
            if Plant.state == 2:
                return pygame.image.load("tiles\sunflower_II.png").convert()
            if Plant.state == 3:
                return pygame.image.load("tiles\sunflower_III.png").convert()
            if Plant.state == 4:
                return pygame.image.load("tiles\sunflower_IV.png").convert()

    
def main():

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    s = Sunflower()

    a = Tile()

    

    pygame.display.flip()
    status = True
    while (status):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                status = False


        if random.randint(0,100) == 100:
            s.grow()

        screen.blit(a.show(s), (0, 0))


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()