'''
Created on 2015. 6. 15.

@author: jongyeob
'''
from __future__ import absolute_import

from ConfigParser import SafeConfigParser

__all__ = ['load','set','get']

def load(file):
    items = {}
    config = SafeConfigParser()
    config.read(file)
    for sec in config.sections():
        items[sec] = dict(config.items(sec))
        
    return items
def set(items,**kwargs):
    '''
    parameters:
        ns - dict : namespace
    '''
    for key in kwargs:     
        items[key] = kwargs[key]
        
def get(items,key):
    return dict([ (itemkey,items[itemkey]) for itemkey in items if itemkey.startswith(key)] )
