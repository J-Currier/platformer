import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    #controls enemy sprites
    def __init__(self, pos, size, *my_path):
        super().__init__(pos, size, *my_path)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 5)
        
    def move(self):
        #makes enemy walk using random speed
        self.rect.x += self.speed
        
    def reverse_image(self):
        #flips enemy image when walking to the left
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            
    def reverse(self):
        #reverses walking direction
        self.speed *= -1
            
    def update(self, shift):
        #updates sprite position and image in game
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()