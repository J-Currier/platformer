from turtle import speed
import pygame
from particles import ParticleEffect
from tiles import Tile, StaticTile, Crate, Coin
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect
from support import import_csv_layout, import_cut_graphics
from os import path


class Level:
    def __init__(self, level_data, surface):
        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0
        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        #terrain layout level arcitecture lu 
        terrain_layout= import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        #grass set up
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        
        #crates set up
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')
        
        #coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for item_index, item in enumerate(row):
                if item != '-1':
                    x = item_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain': 
                        terrain_tile_list = import_cut_graphics('graphics', 'terrain', 'terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(item)]
                        sprite = StaticTile( (x, y), tile_size, tile_surface)
                        
                        
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics', 'decoration', 'grass', 'grass.png')
                        tile_surface = grass_tile_list[int(item)]
                        sprite = StaticTile( (x, y), tile_size, tile_surface)
                       
                        
                    if type == 'crates':
                        sprite = Crate((x, y), tile_size)
                        
                        
                    if type == 'coins':
                        print('im a coin')
                        if item == '0':
                            sprite = Coin((x, y), tile_size, 'graphics', 'coins', 'gold')
                        if item == '1':
                            sprite = Coin((x, y), tile_size, 'graphics', 'coins', 'silver')
                        
                        
                        
                    sprite_group.add(sprite)
            
            
        return sprite_group
        
   
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, 5)
            
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)
    
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True 
        else: 
            self.player_on_ground = False
    
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
               offset = pygame.math.Vector2(10, 15)

            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)
            
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle() #LU why add this? 28:09
        
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index*tile_size #left right position
                y = row_index*tile_size #up down position

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles) #LU passing a method to a child
                    self.player.add(player_sprite)
                    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < (screen_width/5) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width * 4/5) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else: 
            self.world_shift = 0
            player.speed = 8
            
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0: #rt sided collisoin
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0 :
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0 : #downward movement
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 #stops gravity from compunding if player is motionless
                    player.on_ground = True
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            '''checking if player is jumping or falling and switching of on ground'''
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
                       
    def run(self):
        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)
        
        #level tiles (vid1)
        #remove? tiles.update
        self.tiles.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        #grass 
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        #self.tiles.draw(self.display_surface)
        #vid2
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        #crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)
        
        #coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        
        
        


        #player sprite
        self.player.update()
        self.scroll_x()
        self.horizontal_movement_collision()
        self.get_player_on_ground() #checks if player on ground before vert collision
        self.vertical_movement_collision()
        self.create_landing_dust()
        
       
        
        self.player.draw(self.display_surface)
        
        
