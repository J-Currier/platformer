import pygame
from support import import_folder
from os import path

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assests()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16 #neagtive b/c player jumps UP
        
        #player status
        self.status = 'idle'
        self.facing_right = True 
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
    def import_character_assests(self):
        my_path = path.join("graphics", "character")
        character_path = '../graphics/character/'#changed
        self.animations = {'idle':[],
                           'run':[], 
                           'jump':[], 
                           'fall':[]}
        
        for animation in self.animations.keys():
            my_full_path = path.join(my_path, animation)
            #full_path = character_path + animation
            self.animations[animation] = import_folder(my_full_path)
    
    def animate(self): 
        animation = self.animations[self.status]
        
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else: 
            flipped_image = pygame.transform.flip(image, True, False) #(surface, flip horiz., flip vert.)
            self.image = flipped_image
            
        #set origin point for animation png on rect
        if self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)
        
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
        
        if keys[pygame.K_SPACE]:
            self.jump()
    
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
        self.rect.y += self.direction.y
    
    def jump(self):
        self.direction.y = self.jump_speed
    
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
