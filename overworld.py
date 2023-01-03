import pygame
from gamedata import levels 
from os import path
from support import import_folder
from decoration import Sky


class Node(pygame.sprite.Sprite):
    #creates nodes for each level
    def __init__(self, pos, status, icon_speed, mypath):
        super().__init__()
        mypaths = path.join(*mypath)
        self.frames = import_folder(mypaths)
        self.frame_index = 0
        self.image = self.frames[self.frame_index] 
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)
        #target rect needs to be h and w = to speed so that icon doesn't over shoot without triggering a collision
        self.detection_zone = pygame.Rect((self.rect.centerx - (icon_speed/2)), (self.rect.centery - (icon_speed/2)), icon_speed, icon_speed)
        
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def update(self):
        if self.status== 'available':
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surface, (0,0))
            
class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(path.join('graphics', 'overworld', 'hat.png')).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        
    def update(self):
        #adjusts rect of player icon position to account for int conversion when placing the level rectangle/icon on the screen
        self.rect.center = self.pos
        
class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        super().__init__()
        #setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        
        #movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        
        #sprites
        self.setup_nodes()
        self.setup_icon()
        
        #time 
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300
        
        
        
    def setup_nodes(self):
        #creates level nodes and either locks or opens them based on current level completed
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                print(node_data['node_graphics'], 'node data')
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics']) #*******         
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(node_sprite)
            
    def draw_paths(self):
        #make a list of points up to open level (below max level)
        points = []
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                points.append(node_data['node_pos'])
        if len(points) > 1:        
            pygame.draw.lines(self.display_surface, '#a04f45', False,  points, 12)
        
    def setup_icon(self):
        #creates the player sprite
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
 
    def input(self):
        #detects if key is being pressed and adjusts the current level accordingly
        keys = pygame.key.get_pressed()
        
        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
                print(self.current_level)
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('last')
                self.current_level -= 1
                self.moving = True
                print(self.current_level)

            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)
                
    def get_movement_data(self, target):
        #calculates the degree of the path between nodes
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        
        return (end - start).normalize()
        
    
    def update_icon_pos(self):
        #moves icon from one level node to another after player presses key
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time >= self.start_time + self.timer_length:
                self.allow_input = True
                   
    
    def run(self):
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()
        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        
        
        