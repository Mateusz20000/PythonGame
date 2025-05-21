import pygame

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
                return pygame.image.load("tiles\hay_I.png").convert_alpha()
            if self.state == 2:
                return pygame.image.load("tiles\hay_II.png").convert_alpha()
            if self.state == 3:
                return pygame.image.load("tiles\hay_III.png").convert_alpha()
            if self.state == 4:
                return pygame.image.load("tiles\hay_V.png").convert_alpha()
            if self.state == 5:
                return pygame.image.load("tiles\hay_V.png").convert_alpha()


class Corn:

    def __init__(self):
        self.state = 1
        self.name = "corn"

    def grow(self):
        
        if self.state < 4:
            self.state += 1
    
    def show(self):

        if self.name == "corn" :
            if self.state == 1:
                return pygame.image.load("tiles\corn_I.png").convert_alpha()
            if self.state == 2:
                return pygame.image.load("tiles\corn_II.png").convert_alpha()
            if self.state == 3:
                return pygame.image.load("tiles\corn_III.png").convert_alpha()
            if self.state == 4:
                return pygame.image.load("tiles\corn_IV.png").convert_alpha()




class Pumpkin:

    def __init__(self):
        self.state = 1
        self.name = "pumpkin"

    def grow(self):
        
        if self.state < 6:
            self.state += 1
    
    def show(self):

        
        if self.state == 1:
            return pygame.image.load("tiles\pumpkin_I.png").convert_alpha()
        if self.state == 2:
            return pygame.image.load("tiles\pumpkin_II.png").convert_alpha()
        if self.state == 3:
            return pygame.image.load("tiles\pumpkin_III.png").convert_alpha()
        if self.state == 4:
            return pygame.image.load("tiles\pumpkin_IV.png").convert_alpha()
        if self.state == 5:
            return pygame.image.load("tiles\pumpkin_V.png").convert_alpha()
        if self.state == 6:
            return pygame.image.load("tiles\pumpkin_VI.png").convert_alpha()
