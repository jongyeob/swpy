'''
Created on 2013. 11. 9.

@author: Daniel
'''
import logging
LOG = logging.getLogger(__name__)

import sys,os,glob,math
from os import path
import datetime
import sys
import date_time as dt
from config import Config

class NullHandler(logging.Handler): # Compatiable for > 2.7
    def emit(self,record): pass

if 'NullHandler' not in dir(logging):
    logging.NullHandler = NullHandler

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

    for _t in dt.series(start,end,**dt.get_least_delta(dir_format)):
        data_dir = dt.replace(dir_format,_t)    
        _files = get_files(data_dir+'/*')
        files.extend(_files)

    files.sort()
    datetime_parser = lambda p:dt.parse_string(path_format,p)
    ret = dt.filter(files,start_datetime,end_datetime,cadence,datetime_parser=datetime_parser)
        
    return ret

def replace(format_string,**kwargs):
    '''
    Replace a string from formats defined as %(...)  
    '''
    
    f = format_string    

    for k in kwargs.iterkeys():
        i = f.find('$('+k+')') # i : index
        while(i != -1): 
            i2 = i + len(k)+3
            f = f[:i] + kwargs[k] + f[i2:]
            i = f.find('$('+k+')') 
        
    return f
    
def import_all(name,globals={},locals={}):
    try:
        pkg   = __import__(name)
        for key in pkg.__all__:
            globals[key] = getattr(pkg,key)
            locals[key]  = getattr(pkg,key)
            LOG.info('Import %s in %s'%(key,name))
    except Exception as err:
        LOG.error('Download package is not loaded : %s'%(str(err)))
        return False
    
    return True

def get_logger(name='',level=0,handler=logging.NullHandler()):
    if name == '__main__':
        name = ''
        
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
    
def print_out(msg):
    sys.stdout.write(msg+'\n')
def print_err(msg):
    sys.stderr.write(msg+'\n')
def get_files(path_exp):
    # path_exp : expression of path
    arg_path = path.split(path_exp)
                
    file_list = []
    for dirname,_,_ in os.walk(arg_path[0]):
        for filepath in glob.glob(dirname+'/'+ arg_path[1]):
            filepath = filepath.replace('\\','/')
            file_list.append(filepath)
        
    return file_list
   
def make_dirs(pathstr):
    pathstr = path.normpath(pathstr+'/')
    if path.exists(pathstr) == False:
        os.makedirs(pathstr)

def make_path(pathstr):    
    pathstr = path.normpath(pathstr)
    dirpath,filename = path.split(pathstr)

    if len(dirpath) > 0 and path.exists(dirpath) == False:
        os.makedirs(dirpath)
        
    return pathstr

def alert_message(message):
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "    " + message)
    
def great_circle_distance(lon,lat,lon2=0,lat2=0):
    dlon,dlat = (lon2-lon)/2.,(lat2-lat)/2.
    
    sindis = math.sqrt(math.sin(dlat)*math.sin(dlat)+math.cos(lon)*math.cos(lon2)*math.sin(dlon)*math.sin(dlon))
    return 2.0*math.asin(sindis)


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
        temp = int(math.floor(num / 1000000000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000000000

    if (num >= 1000000000):
        temp = int(math.floor(num / 1000000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000000

    if (num >= 1000000):
        temp = int(math.floor(num / 1000000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000000

    if (num >= 1000):
        temp = int(math.floor(num / 1000))
        if (len(str_num) > 0): str_num += "%03d,"%(temp)
        else: str_num += "%d,"%(temp)
        num = num - temp * 1000

    if (len(str_num) > 0): str_num += "%03d"%(num)
    else: str_num += "%d"%(num)

    return str_num
