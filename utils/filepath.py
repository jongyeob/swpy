'''
Created on 2015. 6. 16.

@author: jongyeob
'''
import os
import glob
import date_time as dt
from os import path
import shutil
 
import tempfile

__all__ = ['glob','path','make_dirs','make_path','get_files','request_files','mkpath','mkdirs']

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
   
def request_files(path_format,start_datetime,end_datetime='',cadence=0):
    '''
    request files
    
    parameters:
        path_format - string 
        start_datetime - string
    optional:
        end_datetime   - string
        cadence        - number, seconds
    returns:
        (list) filepath
    '''
        
    start   = dt.parse(start_datetime)
    end     = start 
    dir_format,file_format = path.split(path_format)
        
    if end_datetime != '':
        end = dt.parse(end_datetime)
              
    files = []
    
    least_delta = dt.get_least_delta(dir_format)

    for _t in dt.series(start,end,**least_delta):
        data_dir = dt.replace(dir_format,_t)    
        _files = get_files(data_dir+'/*')
        files.extend(_files)

    files.sort()
    datetime_parser = lambda p:dt.parse_string(path_format,p)
    ret = [f[0] for f in dt.filter(files,start_datetime,end_datetime,cadence,time_parser=datetime_parser)]
        
    return ret

make_path = mkpath
make_dirs = mkdirs
