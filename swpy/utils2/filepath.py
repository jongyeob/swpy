'''
Created on 2016. 10. 20.

@author: jongyeob
'''
import os as _os
import glob as _glob


from os.path import normpath,exists,split


def mkdirs(pathstr):
    pathstr = normpath(pathstr+'/')
    if exists(pathstr) == False:
        _os.makedirs(pathstr)

def mkpath(pathstr):    
    pathstr = normpath(pathstr)
    dirpath,filename = split(pathstr)

    if len(dirpath) > 0 and exists(dirpath) == False:
        _os.makedirs(dirpath)
        
    return pathstr

def get_files(path_exp):
    # path_exp : expression of path
    arg_path = split(path_exp)
                
    file_list = []
    for dirname,_,_ in _os.walk(arg_path[0]):
        for filepath in _glob.glob(dirname+'/'+ arg_path[1]):
            filepath = filepath.replace('\\','/')
            file_list.append(filepath)
        
    return file_list