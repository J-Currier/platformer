import pygame
from particles import ParticleEffect
from tiles import Tile, StaticTile, Crate, Coin, Palm
from settings import tile_size, screen_width, screen_height
from player import Player
from particles import ParticleEffect
from support import import_csv_layout, import_cut_graphics
from os import path
from enemy import Enemy
from decoration import Sky, Water, Cloud
from gamedata import levels
from time import sleep



class Level:
    def __init__(self, current_level, surface, create_overworld, change_coin, change_health):
        #level setup
        self.create_overworld = create_overworld
        self.current_level = current_level
        self.level_data = levels[self.current_level]
        self.display_surface = surface
        #self.setup_level(self.level_data)
        self.tiles = pygame.sprite.Group()
        self.world_shift = 0
        self.current_x = None
        self.new_max_level = self.level_data['unlock']
        
        #audio
        self.coin_sound = pygame.mixer.Sound(path.join('audio', 'effects', 'coin.wav'))
        self.stomp_sound = pygame.mixer.Sound(path.join('audio', 'effects', 'stomp.wav'))
        
        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
        #explosion particles
        self.explosion_sprites = pygame.sprite.Group()

        #player
        player_layout= import_csv_layout(self.level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)
        
        #UI
        self.change_coins = change_coin
        self.change_health = change_health
        
        #terrain layout level arcitecture lu 
        terrain_layout= import_csv_layout(self.level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        #grass set up
        grass_layout = import_csv_layout(self.level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        
        #crates set up
        crate_layout = import_csv_layout(self.level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')
        
        #coins
        coin_layout = import_csv_layout(self.level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        
        #palmtrees foreground
        fg_palm_layout = import_csv_layout(self.level_data['fg_palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg_palms')
        
        #palmtrees foreground
        bg_palm_layout = import_csv_layout(self.level_data['bg_palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg_palms')
        
        #enemies
        enemy_layout = import_csv_layout(self.level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        
        #enemy constraint
        constraint_layout = import_csv_layout(self.level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')
        
        #sky
        self.sky = Sky(8)
        level_width = len(terrain_layout[0] * tile_size)
        self.clouds = Cloud( 400, level_width, 22)
        
        #water
        self.water = Water((screen_height - 20), level_width)
        
    def level_switch(self):
        #exits level to overworld 
        keys = pygame.key.get_pressed()
        #enter key to count as win
        if keys[pygame.K_RETURN]:
            self.current_level += 1
            self.create_overworld(self.current_level)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level)
        
    def create_tile_group(self, layout, type):
        #creates the image tiles based on the csv files
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
                        if item == '0':
                            sprite = Coin((x, y), tile_size, 5, 5, 'graphics', 'coins', 'gold')
                        if item == '1':
                            sprite = Coin((x, y), tile_size, 1, 1,'graphics', 'coins', 'silver')
                        
                    if type == 'fg_palms':
                        if item == '0':
                            sprite = Palm((x, y), tile_size, 38, 'graphics', 'terrain', 'palm_small')
                        if item == '1':
                            sprite = Palm((x, y), tile_size, 64, 'graphics', 'terrain', 'palm_large')
                            
                    if type == 'bg_palms':
                        sprite = Palm((x, y), tile_size, 64, 'graphics', 'terrain', 'palm_bg')
                        
                    if type == 'enemies':
                        sprite = Enemy((x, y), tile_size, 1, 'graphics', 'enemy', 'run')
                        
                    if type == 'constraints':
                        sprite = Tile((x, y), tile_size)
                        
                    sprite_group.add(sprite)
        return sprite_group
    
    def player_setup(self, layout, change_health):
        #adds player sprite and hat/end point to level
        for row_index, row in enumerate(layout):
            for item_index, item in enumerate(row):
                x = item_index * tile_size
                y = row_index * tile_size

                if item == '1':
                    #player sprite
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                if item == '2':
                    #hat sprite
                    hat_surface = pygame.image.load(path.join('graphics', 'character', 'hat.png')).convert_alpha()
                    sprite = StaticTile((x, y), tile_size, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        #checks for enemy sprite colliding with constraint barrier and reverses enemy direction
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()
        
    def create_jump_particles(self, pos):
        #calls the dust particles when player jumps
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, 5)
            
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)
    
    def get_player_on_ground(self):
        #checks if player on ground and changes level class player on ground variable to reflect it
        if self.player.sprite.on_ground:
            self.player_on_ground = True 
        else: 
            self.player_on_ground = False
    
    def create_landing_dust(self):
        #calls dust particles for when player lands 
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
               offset = pygame.math.Vector2(10, 15)

            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)
            
    def scroll_x(self):
        #scrolls the world when player enters left/right-most 25% of screen
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < (screen_width/4) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width * 3/4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else: 
            self.world_shift = 0
            player.speed = 8
            
    def horizontal_movement_collision(self):
        #checks for player collison with terrain, palm, and crate sprites
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        
        for sprite in collidable_sprites:
            #checks for collision betwen sprite and the colidable rect of player(doesn't include sword)
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0: #rt sided collisoin
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
       
    def vertical_movement_collision(self):
        #checks for verticle collision between player and palm, terrian, crates
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y < 0 :
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0 : #downward movement
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0 #stops gravity from compunding if player is motionless
                    player.on_ground = True
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            #checking if player is jumping or falling and switching off on ground
            player.on_ground = False
     
    def check_death(self):
        #checks if player has fallen below bottom of screen
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level)
        
    def check_win(self):
        #checks if player has collided with hat/end sprite
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.current_level += 1 
            #pause before launching overworld
            sleep(.5)
            self.create_overworld(self.current_level)
        
    def check_coin_collisions(self):
        #checks if player collides with coins and calls the function to add to coin total
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)
        
    def check_enemy_collisons(self):
        #check for collision between player and enemy
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        
        if enemy_collisions:
            for enemy in enemy_collisions:
                self.stomp_sound.play()
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom 
                #checks if player is on top of enemy and palyer is moving down onto enemy
                #if yes, player kills enemy, if not -enemy damages player  
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explode')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()
                      
    def run(self):
        #level checks
        self.check_win()
        self.check_death()
        self.level_switch()
        
        #sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        
        #palms background
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        #level tiles 
        self.tiles.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        #enemies
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        #grass 
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        #coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        
        #palms foreground
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)
        
        #goal sprite
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
    
        #player collision
        self.check_coin_collisions()
        self.check_enemy_collisons()

        #player sprite
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()
        self.horizontal_movement_collision()
        self.get_player_on_ground() #checks if player on ground before vert collision
        self.vertical_movement_collision()
        self.create_landing_dust()
        
        #water
        self.water.draw(self.display_surface, self.world_shift)
        
        #draw player
        self.player.draw(self.display_surface)