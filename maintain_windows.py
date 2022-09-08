import os
import shutil
import pathlib

path = input("please enter path")
def list_file(path_):
    for i in os.listdir(path_):
        if os.path.isfile(path_+"/"+i):
            check_extension(i,path_)

def check_extension(file,path_):
        filename, ext =  os.path.splitext(path_+"/"+file)
        if ext != "" :
           create_dir(file,path_,ext)

def create_dir(filename,path_,ext):
       dir = ext.replace(".","")
       isdir = os.path.isdir(path_+"/"+dir)
       if isdir is False :
           os.mkdir(path_+"/"+dir)
       move_file(filename,path_,dir)    

def move_file(file,path_,extension):
       dest = shutil.move(path_+"/"+file,path_+"/"+extension) 


list_file(path)        