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
            
class Icon(pygame.sprite.Sprite):
     def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill('dark green')
        self.rect = self.image.get_rect(center = pos)
        
class Overworld:
    def __init__(self, start_level, max_level, surface):
        super().__init__()
        #setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        
        #sprites
        self.setup_nodes()
        self.setup_icon()
        
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available')           
            else:
                node_sprite = Node(node_data['node_pos'], 'locked')
            self.nodes.add(node_sprite)
            
    def draw_paths(self):
        #make a list of points up to open level (below max level)
        points = []
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                points.append(node_data['node_pos'])
                
                
        pygame.draw.lines(self.display_surface, 'purple', False,  points, 6)
        
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
 
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
            self.current_level += 1
        elif keys[pygame.K_LEFT] and self.current_level > 0:
            self.current_level -= 1
    
    def update_icon_pos(self):
        self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center

    def run(self):
        self.input()
        self.update_icon_pos()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        
        
        