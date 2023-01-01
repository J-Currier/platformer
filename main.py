import pygame, sys
from settings import *
from tiles import Tile
from level import Level
from gamedata import levels
from overworld import Overworld

class Game:
    def __init__(self):
        self.max_level = 3
        self.current_level = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        

    def create_level(self, current_level):
        self.current_level = current_level
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'level'
    
    def create_overworld(self, level_pos):
        self.current_level = level_pos
        self.overworld = Overworld(level_pos, self.max_level, screen, self.create_level)
        self.status = 'overworld'

              
              
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()   
        else:
            self.level.run()
    
#pygame set up
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
#level = Level(levels[0], screen)
game = Game() #takeout

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill('black')
    game.run()
    #level.run() #take out
    
    pygame.display.update()
    clock.tick(60)