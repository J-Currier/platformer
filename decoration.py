import pygame
from os import path
from settings import vertical_tile_height, tile_size, screen_width
from tiles import  AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint


class Sky:
    #background sky in levels and overworld
    def __init__(self, horizon, style = 'level'):
        self.top = pygame.image.load(path.join('graphics', 'decoration', 'sky', 'sky_top.png')).convert()
        self.bottom = pygame.image.load(path.join('graphics', 'decoration', 'sky', 'sky_bottom.png'))
        self.middle = pygame.image.load(path.join('graphics', 'decoration', 'sky', 'sky_middle.png'))
        self.horizon = horizon
        
        #horizontal stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))
        self.style = style
        
        #adds b.g. clouds and palms in overworld background
        if self.style == 'overworld':
            palm_surface = import_folder(path.join('graphics', 'overworld', 'palms'))
            self.palms = []
            for surface in [choice(palm_surface) for image in range(10)]:
                x = randint( 0, screen_width)
                y = (self.horizon * tile_size) + randint(50, 100)
                rect = surface.get_rect(midbottom = (x, y))
                self.palms.append((surface, rect))
                
            cloud_surface = import_folder(path.join('graphics', 'overworld', 'clouds'))
            self.clouds = []
            for surface in [choice(cloud_surface) for image in range(6)]:
                x = randint( 0, screen_width)
                y =  randint(0, (self.horizon * tile_size)- 100 )
                rect = surface.get_rect(midbottom = (x, y))
                self.clouds.append((surface, rect))
            
        
    def draw(self, surface):
        #draws the sky/orizon/bottom layer in level and overworld
        for row in range(vertical_tile_height):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))
        
        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])  
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1]  )    
    
    
class Water: 
    #makes water for levels
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + (2 *screen_width)) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()
        
        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile((x, y), 192, 2, 'graphics', 'decoration', 'water')
            self.water_sprites.add(sprite)
    
    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


class Cloud:
    #draws clouds in background of levels
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder(path.join('graphics', 'decoration', 'clouds'))
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()
        
        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile((x, y), 1, cloud) #~2:49 in second vid
            self.cloud_sprites.add(sprite)
            
    def draw(self, surface, shift):
        #draws the clouds
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
        
            
            