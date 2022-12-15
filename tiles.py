#sprite (tiles)

import pygame
import os 
from settings import tile_size


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, x_shift):
    #provides logic to scroll left/rt through level
        self.rect.x += x_shift
        
class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface
        
class Crate(StaticTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load(os.path.join('graphics', 'terrain', 'crate.png')).convert_alpha()) #LU make sure no path error
        offset_y = pos[1] + tile_size
        self.rect = self.image.get_rect(bottomleft = (pos[0], offset_y))
        print('crate position error')
        