#sprite (tiles)

import pygame
import os 
from settings import tile_size
from support import import_folder


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

class AnimatedTile(Tile):
    def __init__(self, pos, size, *my_path):
        super().__init__(pos, size)
        print(my_path, type(my_path), 'myp')   
        print('print', os.path.join(*my_path))
        self.frames = import_folder(os.path.join(*my_path))
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
        
class Coin(AnimatedTile):
    def __init__(self, pos, size, *my_path):
        super().__init__(pos, size, *my_path)
        center_x = pos[0] + int(tile_size / 2)
        center_y = pos[1] + int(tile_size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        
        
            