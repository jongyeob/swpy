'''
Created on 2015. 6. 15.

@author: jongyeob
'''
from ConfigParser import SafeConfigParser
from types import ModuleType

__all__ = ['load','set','get']

def load(file):
    items = {}
    config = SafeConfigParser()
    config.read(file)
    for sec in config.sections():
        items[sec] = dict(config.items(sec))
        
    return items

def set(ns,keymap={},**kwargs):
    '''
    parameters:
        ns - dict : namespace
    '''
    get = dict.get
    set = dict.setdefault
    list = dict.keys
    
    if isinstance(ns,ModuleType):
        get = getattr
        set = setattr
        list = dir
    
    if not keymap:
        keymap = dict([(k.lower(),k) for k in list(ns)])
    
    for key in kwargs:
        option_type = type(get(ns,keymap[key]))
        set(ns,keymap[key],option_type(kwargs[key]))
              
        
def get(items,start):
    return dict([ (key,items[key]) for key in items if key.startswith(start)] )