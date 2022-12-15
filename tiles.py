#sprite (tiles)

import pygame

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
        