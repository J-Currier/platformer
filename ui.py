import pygame
from os import path

class UI:
    def __init__(self, surface):
        
        #setup
        self.display_surface = surface
        self.health_bar = pygame.image.load(path.join('graphics', 'ui', 'health_bar.png'))
        
        #coins
        self.coin = pygame.image.load(path.join('graphics', 'ui', 'coin.png'))
        self.coin_rect = self.coin.get_rect(topleft = (50, 61))
        myfont = path.join('graphics', 'ui', 'ARCADEPI.TTF')
        self.font = pygame.font.Font(myfont, 30)
        
    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))
    
    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, '#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)
