'''
Created on 2013. 11. 9.

@author: Daniel
'''
from __future__ import absolute_import

import datetime
import logging
import sys, math


__all__ = ['get_logger','replace','import_all','alert_message',
           'save_list','save_list_2',
           'get_filename','num2str']

class _NullHandler(logging.Handler): # Compatiable for > 2.7
    def emit(self,record): pass

if 'NullHandler' not in dir(logging):
    logging.NullHandler = _NullHandler


def get_logger(name='',level=0,handler=logging.NullHandler()):
    if name == '__main__':
        name = ''
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger    

def replace(format_string,**kwargs):
    '''
    Replace a string from formats defined as %(...)  
    '''
    
    f = format_string    

    for k in kwargs.iterkeys():
        i = f.find('%('+k+')') # i : index
        while(i != -1): 
            i2 = i + len(k)+3
            f = f[:i] + kwargs[k] + f[i2:]
            i = f.find('%('+k+')') 
        
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

def alert_message(message):
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "    " + message)
    


def save_list(filepath, list):
    
    f = open(filepath, "w")
    for line in list:
        f.write(line + "\n")
    f.close()

    return True


def save_list_2(filepath, list):
    
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


LOG = get_logger(__name__)
