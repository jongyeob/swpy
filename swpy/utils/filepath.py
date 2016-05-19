'''
Created on 2015. 6. 16.

@author: jongyeob
'''
from __future__ import absolute_import

import glob
from os import path
import os
import shutil
import tempfile

from . import datetime as dt


__all__ = ['glob','path','mkdirs','mkpath','get_files','request_files']

class AutoPath(str):
    def __del__(self):
        if path.exists(self):
            shutil.rmtree(self)

def mkdirs(pathstr):
    pathstr = path.normpath(pathstr+'/')
    if path.exists(pathstr) == False:
        os.makedirs(pathstr)

def mkpath(pathstr):    
    pathstr = path.normpath(pathstr)
    dirpath,filename = path.split(pathstr)

    if len(dirpath) > 0 and path.exists(dirpath) == False:
        os.makedirs(dirpath)
        
    return pathstr

def get_files(path_exp):
    # path_exp : expression of path
    arg_path = path.split(path_exp)
                
    file_list = []
    for dirname,_,_ in os.walk(arg_path[0]):
        for filepath in glob.glob(dirname+'/'+ arg_path[1]):
            filepath = filepath.replace('\\','/')
            file_list.append(filepath)
        
    return file_list
   
def request_files(path_format,start_datetime,end_datetime,sample_rate=0,cadence=0):
    '''
    request files
    
    parameters:
        path_format - string 
        start_datetime - string
        end_datetime   - string
    optionals:
        sample_rate    - number[seconds]
        cadence        - deprecated, same as sample_rate
    returns:
        (list) filepath
    '''
    if cadence and not sample_rate:
        sample_rate = cadence
        
    start   = dt.parse(start_datetime)
    end     = dt.parse(end_datetime)
    
    path_format = path_format.replace('\\','/')
    dir_format,file_format = path.split(path_format)
              
    files = []
    
    least_delta = dt.get_least_delta(dir_format)

    for _t in dt.series(start,end,**least_delta):
        data_dir = dt.replace(dir_format,_t)    
        _files = get_files(data_dir+'/*')
        files.extend(_files)

    files.sort()
    time_parser = lambda p:dt.parse_string(path_format,p)
    index = map(time_parser,files)
    ret = dt.filter(zip(index,files),start_datetime,end_datetime,sample_rate)
        
    return ret

make_path = mkpath
make_dirs = mkdirs
