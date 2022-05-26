import pygame
from tiles import Tile
from settings import tile_size
from player import Player

class Level:
    def __init__(self, level_data, surface):
        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
     
     
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index*tile_size #left right position
                    y = row_index*tile_size #up down position
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player = Player((col_index*tile_size,  row_index*tile_size))
                    self.tiles.add(player)
                    
    
       
    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)