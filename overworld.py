import pygame
from gamedata import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((100, 80)) 
        self.image.fill('purple')
        self.rect = self.image.get_rect(center = pos)    
        
        
        
class Overworld:
    def __init__(self, start_level, max_level, surface):
        #setup
        self.display_surface = surface
        self.max_surface = max_level
        self.current_level = start_level
        
        #sprites
        self.setup_nodes()
        
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for node_data in levels.values():
            node_sprite = Node(node_data['node_pos'])
            self.nodes.add(node_sprite)
            
            
            
    def run(self):
        self.nodes.draw(self.display_surface)
        
        pass
        
        