import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI
from os import path

class Game:
    def __init__(self):
        #game attributes
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
        self.current_level = 0

        #audio
        self.play_music = False
        self.level_bg_music = pygame.mixer.Sound(path.join('audio', 'level_music.wav'))
        self.overworld_bg_music =pygame.mixer.Sound(path.join('audio', 'overworld_music.wav'))

        #overworld creation
        self.overworld = Overworld(self.current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        if self.play_music:
            self.overworld_bg_music.play(loops = -1)
            
        #UI 
        self.ui = UI(screen)
        
    def create_level(self, current_level):
        #creates level from overworld
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        if self.play_music:
            self.level_bg_music.play(loops = -1)

    def create_overworld(self, level_pos):
        #creates overwolrd from level
        self.level_bg_music.stop()
        if self.play_music:
            self.overworld_bg_music.play(loops = -1)

        if level_pos <= 5:    
            self.current_level = level_pos
        else:
            self.current_level = 5
        if level_pos > self.max_level:
            self.max_level = level_pos
                        
        self.overworld = Overworld(self.current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def change_coins(self, amount):
        #adds to coin total
        self.coins += amount    
        
    def change_health(self, amount ):
        #changes health status
        self.current_health += amount    
        
    def check_game_over(self):
        #checks if health has reached 0
        if self.current_health <= 0:
            self.current_health = 100
            self.coins = 0
            
            Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            if self.play_music:
                self.overworld_bg_music.play(loops = -1)
                
    '''def toggle_audio():
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_x]:'''
        
    def run(self):
        #runs game
        if self.status == 'overworld':
            self.overworld.run()   
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()
    
#pygame set up
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game() 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    game.run()
    pygame.display.update()
    clock.tick(60) #60 frames for second