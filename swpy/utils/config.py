'''
Created on 2015. 6. 15.

@author: jongyeob
'''
from __future__ import absolute_import

import os
from ConfigParser import RawConfigParser,SafeConfigParser
import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(0)

def get_config(filepath,name,cfg):
    items = load(filepath)
    if items.has_key(name):
        item = items[name]
        num = update(item,cfg)
    else:
        save(filepath,{name:cfg})


    return cfg

def load(filepath):
    items = {}
    config = SafeConfigParser()
    if os.path.exists(filepath):
        f = open(filepath,'r')
        config.readfp(f)
        f.close()
    for sec in config.sections():
        items[sec] = dict(config.items(sec))
        
    return items

def save(filepath,items):
    config = SafeConfigParser()
    f = None
    if os.path.exists(filepath):
        f = open(filepath,'r+')
        config.readfp(f)
        f.seek(0)
    else:
        f = open(filepath,'w')
        
    for sec in items:
        if not config.has_section(sec):
            config.add_section(sec)
        for opt in items[sec]:
            str_value = str(items[sec][opt]) 
            str_value = str_value.replace("%","%%")
            config.set(sec,opt,str_value)

    config.write(f)
    f.close()

def update(src_item,dst_item):
    num_updated = 0
    for key in src_item:
        if not dst_item.has_key(key):
            LOG.debug("Not matching key : %s"%(key))
            continue
        type_item = type(dst_item[key])
        dst_item[key] = type_item(src_item[key])
        num_updated += 1

    return num_updated

def set(items,**kwargs):
    '''
    parameters:
        ns - dict : namespace
    '''
    for key in kwargs:     
        items[key] = kwargs[key]
        
def get(items,key):
    '''
    Retreive item key started with the input key
    '''
    return dict([ (itemkey,items[itemkey]) for itemkey in items if itemkey.startswith(key)] )
