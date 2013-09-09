'''
@summary: Log

@license:    GPLv2
@author:     Jongyeob Park(pjystar@gmail.com)
@version:    2013-08-06
'''
import sys
from os.path import split,join
from datetime import datetime


CRITICAL  = 50
ERROR     = 40
WARNING   = 30
INFO      = 20
DEBUG     = 10
UNSET     = 0

LEVELS = {CRITICAL:'CRITICAL',ERROR:'ERROR',WARNING:'WARNING',INFO:'INFO',DEBUG:'DEBUG',UNSET:'UNSET'}

g_level = 0
g_path = None

def config(level=30,path=None):
    global g_level,g_path
    g_level = level
    g_path = path
    
def issue(msg,level=UNSET):    
    
    level_str = 'UNSET'
    if isinstance(level,int) == True:
        level = UNSET
        
    if LEVELS.has_key(level) == True:
        level_str = LEVELS[level]
    
    now = datetime.now()
    if level >= g_level:
        msg = '%s [%s] : %s\n'%(now.strftime("%Y%m%d_%H%M%S"),level_str,msg)
        sys.stderr.write(msg)
        
        if g_path is not None :
            dirname,filename = split(g_path)
            if len(filename) == 0:
                filename = now.strftime("%Y%m%d.log")
            
            logpath = join(dirname,filename)
            
            with open(logpath,'a') as f:
                f.write(msg)
                f.close()
            

def write(msg,level=UNSET):    
    if isinstance(level,int) == True:
        level = UNSET
        
    if level >= g_level:
        sys.stderr.write(msg +'\n')