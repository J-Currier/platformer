import os
#from os import walk
#used to import folders using a file system (walk)
#walk returns the directory path, directory names, filenames
import pygame
from csv import reader
from settings import tile_size

def import_folder(path):
    surface_list = []

    for _, __, img_file in os.walk(path):
        for image in img_file:
            ''' import images, put on surface, place the surface in a list, return list'''
            full_path = os.path.join(path, image)
            #full_path = path + '/' + image
            my_surface = pygame.image.load(full_path).convert_alpha()
            #use convert alpha on png files
            surface_list.append(my_surface)
    return surface_list
        
def import_csv_layout(myList):
    path = os.path.join(*myList)
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
                    
def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha() #LU
    tile_num_x = int(surface.get_size()[0]/tile_size)
    tile_num_y = int(surface.get_size()[1]/tile_size)
    
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.surface((tile_size, tile_size))
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
        
    return cut_tiles  
