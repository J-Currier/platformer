import pygame
from gamedata import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__()

        self.image = pygame.Surface((100, 80)) 
        if status == 'available':
            self.image.fill('purple')
        else:
            self.image.fill('dark blue')
        self.rect = self.image.get_rect(center = pos)
            
        
        
        
class Overworld:
    def __init__(self, start_level, max_level, surface):
        #setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        
        #sprites
        self.setup_nodes()
        
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available')           
            else:
                node_sprite = Node(node_data['node_pos'], 'locked')
            self.nodes.add(node_sprite)
            
    def draw_paths(self):
        
        pygame.draw.line(self.display_surface, 'purple', False,  points, 6
 
            
    def run(self):
        self.nodes.draw(self.display_surface)
        
        pass
        
        