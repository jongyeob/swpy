'''
Created on 2016. 10. 20.

@author: jongyeob
'''
import os
import glob
import logging

LOG = logging.getLogger(__name__)


def mkdirs(pathstr):
    pathstr = os.path.normpath(pathstr+'/')
    if os.path.exists(pathstr) == False:
        os.makedirs(pathstr)

def mkpath(pathstr):    
    pathstr = os.path.normpath(pathstr)
    dirpath,filename = os.path.split(pathstr)

    if len(dirpath) > 0 and os.path.exists(dirpath) == False:
        os.makedirs(dirpath)
        
    return pathstr

def get_files(path_exp):
    # path_exp : expression of path
    arg_path = os.path.split(path_exp)
                
    file_list = []
    for dirname,_,_ in os.walk(arg_path[0]):
        for filepath in glob.glob(dirname+'/'+ arg_path[1]):
            filepath = filepath.replace('\\','/')
            file_list.append(filepath)
        
    return file_list

