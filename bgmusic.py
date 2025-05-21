import pygame
import sys

pygame.init()
pygame.mixer.init()

playlist = [
    "bgplaylist/Wake-up.ogg",
    "bgplaylist/The-Farmer.ogg",
    "bgplaylist/Happy-Farm.ogg",
    "bgplaylist/The-Farmer.ogg"
]

current_track = 0

def play_next():
    global current_track
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.set_volume(0.08)
    pygame.mixer.music.play()
    current_track = (current_track + 1) % len(playlist)

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

#screen = pygame.display.set_mode((800, 600))  (Test)
#pygame.display.set_caption("Test")            

class Music:
    def __init__(self):

        play_next()
    
    def start(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == MUSIC_END:
                    play_next()

    #screen.fill((0, 0, 0))                    (Test)
    #pygame.display.flip()

        pygame.quit()
        sys.exit()


