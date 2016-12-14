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
<<<<<<< HEAD
def set(ns,**kwargs):
=======
def set(items,**kwargs):
>>>>>>> bd9b3820ca2d2e063f3be5fc53fc4b1f16fb71ef
    '''
    parameters:
        ns - dict : namespace
    '''
    for key in kwargs:     
<<<<<<< HEAD
        ns[key] = kwargs[key]
        
def get(items,start):
    return dict([ (key,items[key]) for key in items if key.startswith(start)] )
=======
        items[key] = kwargs[key]
        
def get(items,key):
    return dict([ (itemkey,items[itemkey]) for itemkey in items if itemkey.startswith(key)] )
>>>>>>> bd9b3820ca2d2e063f3be5fc53fc4b1f16fb71ef
