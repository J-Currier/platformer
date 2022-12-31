import pygame
from gamedata import levels


class Node(pygame.sprite.Sprite):
    #creates nodes for each level
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
        self.pos = pos
        self.image = pygame.Surface((20, 20))
        self.image.fill('dark green')
        self.rect = self.image.get_rect(center = pos)
        
    def update(self):
        #adjusts rect of player icon position to account for int conversion when placing the level rectangle/icon on the screen
        self.rect.center = self.pos
        
class Overworld:
    def __init__(self, start_level, max_level, surface):
        super().__init__()
        #setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        
        #movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        
        #sprites
        self.setup_nodes()
        self.setup_icon()
        
    def setup_nodes(self):
        #creates level nodes and either locks or opens them based on current level completed
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
        #creates the player sprite
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
 
    def input(self):
        #detects if key is being pressed and adjusts the current level accordingly
        keys = pygame.key.get_pressed()
        
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data()
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.current_level -= 1
                self.moving = True

            
    def get_movement_data(self):
        #calculates the degree of the path between nodes
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        
        return (end - start).normalize()
        
    
    def update_icon_pos(self):
        #moves icon from one level node to another after player presses key
        self.icon.sprite.pos += self.move_direction * self.speed
    
    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        
        
        