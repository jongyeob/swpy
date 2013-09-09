'''
@summary: system

@license:    GPLv2
@author:     Jongyeob Park(pjystar@gmail.com)
@version:    2013-08-06
'''
import os,glob
from os import path

def get_files(path_exp):
    # path_exp : expression of path
    arg_path = os.path.split(path_exp)
                
    file_list = []
    for dirname,_,_ in os.walk(arg_path[0]):
        for filepath in glob.glob(os.path.join(dirname,arg_path[1])):
            file_list.append(filepath)
        
    return file_list

def make_dirs(dirpath):
    if path.exists(dirpath) == False:
        os.makedirs(dirpath)

def prepare_dirs(filepath):
    dirname,_ = os.path.split(filepath)
    make_dirs(dirname)