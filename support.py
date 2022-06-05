from os import walk #used to import folders using a file system (walk)
#walk returns the directory path, directory names, filenames

def import_folder(path):
    print("here")

    for myinfo in walk(path):
        print(list(myinfo))
        print("hi")
        
import_folder('graphics/character/run')
