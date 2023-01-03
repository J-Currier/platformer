import pygame
from support import import_folder
from os import path
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()
        self.import_character_assests()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        self.change_health = change_health
        self.invincible = False
        self.invincible_duration = 500
        self.hurt_time = 0
        
 
        #dust particles       
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16 #neagtive b/c player jumps UP
        self.collision_rect =pygame.Rect(self.rect.topleft, (50, self.rect.height))
        
        #player status
        self.status = 'idle'
        self.facing_right = True 
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
    def import_character_assests(self):
        my_path = path.join("graphics", "character")
        #character_path = '../graphics/character/'#changed
        self.animations = {'idle':[],
                           'run':[], 
                           'jump':[], 
                           'fall':[]}
        
        for animation in self.animations.keys():
            my_full_path = path.join(my_path, animation)
            print(my_full_path, "myfullpath")
            #full_path = character_path + animation
            self.animations[animation] = import_folder(my_full_path)

    def import_dust_run_particles(self):
        my_path = path.join("graphics", "character", "dust_particles", "run")
        self.dust_run_particles = import_folder(my_path)
            
            
    def animate(self): 
        animation = self.animations[self.status]
        
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else: 
            flipped_image = pygame.transform.flip(image, True, False) #(surface, flip horiz., flip vert.)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright
        
        #flicker effect for invincibility
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else: self.image.set_alpha(255)  
        
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            
            
            
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index +=  self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)

            else:
                flipped_dust = pygame.transform.flip(dust_particle, True, False) 
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                self.display_surface.blit(flipped_dust, pos)
                
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
    
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle' 
            
    def apply_gravity(self):
        self.direction.y += self.gravity #makes gravity increase every frame
        self.collision_rect.y += self.direction.y
    
    def jump(self):
        self.direction.y = self.jump_speed
        
    def get_damage(self):
        if not self.invincible:   
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            
    def invincible_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time >= self.hurt_time + self.invincible_duration:
                self.invincible = False
    
    def wave_value(self):
        #timer for flickering when player is invincible
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
                 
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincible_timer()
