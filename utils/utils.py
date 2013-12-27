'''
Created on 2013. 11. 9.

@author: Daniel
'''
from __future__ import absolute_import

import os,glob
from os.path import exists,normpath,split
from math import sqrt,sin,cos,asin,floor
import datetime

__all__ =['get_files','make_dirs','with_dirs','alert_message']


def get_files(path_exp):
    # path_exp : expression of path
    arg_path = split(path_exp)
                
    file_list = []
    for dirname,_,_ in os.walk(arg_path[0]):
        for filepath in glob.glob(dirname+'/'+ arg_path[1]):
            file_list.append(filepath)
        
    return file_list

def make_dirs(dirpath):
    if exists(dirpath) == False:
        os.makedirs(dirpath)

def with_dirs(filepath):
    filepath = normpath(filepath)
    dirname,_ = split(filepath)
    make_dirs(dirname)
    return filepath

def alert_message(message):
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "    " + message)
    
def great_circle_distance(lon,lat,lon2=0,lat2=0):
    dlon,dlat = (lon2-lon)/2.,(lat2-lat)/2.
    
    sindis = sqrt(sin(dlat)*sin(dlat)+cos(lon)*cos(lon2)*sin(dlon)*sin(dlon))
    return 2.0*asin(sindis)


def save_list(filepath, list):
    with_dirs(filepath)
    
    f = open(filepath, "w")
    for line in list:
        f.write(line + "\n")
    f.close()

    return True


def save_list_2(filepath, list):
    with_dirs(filepath)

    list.sort()
    f = open(filepath, "w")
    
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