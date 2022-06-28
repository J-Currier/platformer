import pygame
from support import import_folder
from os import path

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == 'jump':
            my_path = path.join("graphics", "character", "dust_particles", "jump")
            self.frames = import_folder(my_path)
        if type == 'land':
            my_path = path.join("graphics", "character", "dust_particles", "land")
            self.frames = import_folder(my_path)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_Rect(center = pos)
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill() #destoys sprite when animation ends
        else:
            self.image = self.frames[int(self.frame_index)]
        
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

            
    

