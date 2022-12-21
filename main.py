import pygame, sys
from settings import *
from tiles import Tile
from level import Level
from gamedata import levels

class Game:
    def __init__(self):
        self.overworld = Overworld()

    def run(self):
        self.overworld.run()   
    
#pygame set up
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(levels[0], screen)
game = Game() #takeout

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill('black')
    game.run()
    level.run() #take out
    
    pygame.display.update()
    clock.tick(60)