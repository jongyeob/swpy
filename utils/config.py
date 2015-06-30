'''
Created on 2015. 6. 15.

@author: jongyeob
'''
from ConfigParser import SafeConfigParser

__all__ = ['load','set','get']

def load(file):
    items = {}
    config = SafeConfigParser()
    config.read(file)
    for sec in config.sections():
        items[sec] = dict(config.items(sec))
        
    return items
def set(ns,**kwargs):
    '''
    parameters:
        ns - dict : namespace
    '''
    for key in kwargs:     
        option_type = type(ns[key])
        ns[key] = option_type(kwargs[key])
        
def get(items,start):
    return dict([ (key,items[key]) for key in items if key.startswith(start)] )