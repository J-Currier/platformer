import pygame
from os import path
from settings import vertical_tile_height, tile_size, screen_width

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load(path.join('graphics', 'decoration', 'sky', 'sky_top.png')).convert()
        self.bottom = pygame.image.load(path.join('graphics', 'decoration', 'sky', 'sky_bottom'))
        self.middle = pygame.image.load(path.join('graphics', 'decoration', 'sky', 'sky_bottom'))
        self.horizon = horizon
        
        #horizontal stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.top, (screen_width, tile_size))
