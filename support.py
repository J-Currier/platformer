import os
#from os import walk
#used to import folders using a file system (walk)
#walk returns the directory path, directory names, filenames
import pygame
from csv import reader

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
                    
    
