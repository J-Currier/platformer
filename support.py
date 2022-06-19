import os
#from os import walk
#used to import folders using a file system (walk)
#walk returns the directory path, directory names, filenames
import pygame

def import_folder(path):
    print(path, "in import folder func")
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
        
