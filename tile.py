import pygame
import random
import plants


    
    
class Tile:

    def __init__(self, plant):

        self.associate_plant(plant)

    def associate_plant(self, plant):
        
        self.plant = plant
            

tile_width = 64
tile_height = 32

size = 20


def show(screen, grid, size):
        for y in range(size):
            for x in range(size):
                iso_x = (x - y) * (tile_width // 2) + 750
                iso_y = (x + y) * (tile_height // 2) + 100

                screen.blit(grid[y][x].plant.show(), (iso_x, iso_y))


    
def main():

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()



    grid = [[Tile(plants.Pumpkin()) for x in range(size)] for y in range(size)]




    

    pygame.display.flip()
    status = True
    while (status):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                status = False


        for y in range(size):
            for x in range(size):
                
                ran = random.randint(0,250)
                if ran == 10:
                    grid[y][x].plant.grow()

        show(screen, grid, size)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()