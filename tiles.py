import pygame
import os 
from settings import tile_size
from support import import_folder

class Tile(pygame.sprite.Sprite):
    #tile class creates each tile image
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, x_shift):
    #provides logic to scroll left/rt through level
        self.rect.x += x_shift
        
class StaticTile(Tile):
    #for unam=nimated tiles
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface
        
class Crate(StaticTile):
    #class for the crates
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load(os.path.join('graphics', 'terrain', 'crate.png')).convert_alpha()) 
        offset_y = pos[1] + tile_size
        self.rect = self.image.get_rect(bottomleft = (pos[0], offset_y))

class AnimatedTile(Tile):
    #creates tiles for animated tile images
    def __init__(self, pos, size, offset, *my_path):
        super().__init__(pos, size)
        self.frames = import_folder(os.path.join(*my_path))
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
    def animate(self):
        #animates the tile by cycling through frames
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def update(self, x_shift):
        #updates the animated tile
        self.animate()
        self.rect.x += x_shift
        
class Coin(AnimatedTile):
    #class for coin tiles
    def __init__(self, pos, size, value, *my_path):
        super().__init__(pos, size, *my_path)
        self.value = value
        #centres coin in desired position
        center_x = pos[0] + int(tile_size / 2)
        center_y = pos[1] + int(tile_size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
    
class Palm(AnimatedTile):
    #calss for palms
    def __init__(self, pos, size, offset, *my_path):
        super().__init__(pos, size, offset, *my_path)
        offset_y = pos[1] - offset
        self.rect.topleft = (pos[0], offset_y) 
        
            