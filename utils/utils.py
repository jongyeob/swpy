'''
Created on 2013. 11. 9.

@author: Daniel
'''
import logging
LOG = logging.getLogger(__name__)

import os,glob
from os.path import exists,normpath,split
from math import sqrt,sin,cos,asin,floor
import datetime
import sys

def print_out(msg):
    sys.stdout.write(msg+'\n')
def print_err(msg):
    sys.stderr.write(msg+'\n')
def get_files(path_exp):
    # path_exp : expression of path
    arg_path = split(path_exp)
                
    file_list = []
    for dirname,_,_ in os.walk(arg_path[0]):
        for filepath in glob.glob(dirname+'/'+ arg_path[1]):
            file_list.append(filepath)
        
    return file_list
   
def make_dirs(path):
    path = normpath(path+'/')
    if exists(path) == False:
        os.makedirs(path)

def make_path(path):    
    path = normpath(path)
    dirpath,filename = split(path)

    if len(dirpath) > 0 and exists(dirpath) == False:
        os.makedirs(dirpath)
        
    return path

def alert_message(message):
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "    " + message)
    
def great_circle_distance(lon,lat,lon2=0,lat2=0):
    dlon,dlat = (lon2-lon)/2.,(lat2-lat)/2.
    
    sindis = sqrt(sin(dlat)*sin(dlat)+cos(lon)*cos(lon2)*sin(dlon)*sin(dlon))
    return 2.0*asin(sindis)


def save_list(filepath, list):
    
    
    f = open(make_path(filepath), "w")
    for line in list:
        f.write(line + "\n")
    f.close()

    return True


def save_list_2(filepath, list):
    

    list.sort()
    f = open(make_path(filepath), "w")
    
    for line in list:
        f.write(get_filename(line) + "\n")
    
    f.close()

    return True

def get_filename(filepath):
    import string
    
    index = string.rfind(filepath, '/')    # Return -1 on failure
    filename = filepath[index+1:]

    return filename


def num2str(num):
    str_num = ""

    if (num >= 1000000000000):
        temp = int(floor(num / 1000000000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000000000

    if (num >= 1000000000):
        temp = int(floor(num / 1000000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000000

    if (num >= 1000000):
        temp = int(floor(num / 1000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000

    if (num >= 1000):
        temp = int(floor(num / 1000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000

    if (len(str_num) > 0): str_num += "%03d"%(num)
    else: str_num += "%d"%(num)

    return str_num
