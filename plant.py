import pygame
import random

class Sunflower:

    def __init__(self):
        self.state = 1
        self.name = "sunflower"

    def grow(self):
        
        if self.state < 4:
            self.state += 1

class Hay:

    def __init__(self):
        self.state = 1
        self.name = "hay"

    def grow(self):
        
        if self.state < 5:
            self.state += 1
    
    def show(self):

        if self.name == "hay" :
            if self.state == 1:
                return pygame.image.load("tiles\hay_I.png").convert()
            if self.state == 2:
                return pygame.image.load("tiles\hay_II.png").convert()
            if self.state == 3:
                return pygame.image.load("tiles\hay_III.png").convert()
            if self.state == 4:
                return pygame.image.load("tiles\hay_V.png").convert()
            if self.state == 5:
                return pygame.image.load("tiles\hay_V.png").convert()

    
    
class Tile:

    def show(self, Plant):

        if Plant.name == "hay" :
            if Plant.state == 1:
                return pygame.image.load("tiles\hay_I.png").convert()
            if Plant.state == 2:
                return pygame.image.load("tiles\hay_II.png").convert()
            if Plant.state == 3:
                return pygame.image.load("tiles\hay_III.png").convert()
            if Plant.state == 4:
                return pygame.image.load("tiles\hay_V.png").convert()
            if Plant.state == 5:
                return pygame.image.load("tiles\hay_V.png").convert()

    
def main():

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    s = [Hay(), Hay(), Hay(), Hay(), Hay(), Hay(), Hay(), Hay(), Hay(), Hay()]


    

    pygame.display.flip()
    status = True
    while (status):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                status = False


        ran1 = random.randint(0,50)

        if ran1 == 1:
            ran2 = random.randint(0,9)
            s[ran2].grow()



        for i in range(10):
            screen.blit(s[i].show(), (0+i*32, 0+i*16))

        


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()