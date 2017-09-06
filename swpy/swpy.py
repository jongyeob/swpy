'''
Created on 2016. 10. 17.

@author: jongyeob
'''

from __future__ import absolute_import
import os
import logging
from swpy.utils import config
import swpy
import sys

def get_logger(name):
    if not name:
        name = 'swpy'
    elif not name.startswith('swpy.'):
        name = 'swpy.' + name
    
    logger = logging.getLogger(name)
    logger.setLevel(0)
    
    return logger

def get_config(filepath,cfg):
    num = config.get_config(filepath,'swpy',cfg)
    return num

def init(log_level=20,config_file=''):
    if config_file:
        get_config(config_file,swpy.CFG)

    log_handle = logging.StreamHandler(sys.stderr)
    log_format = logging.Formatter(swpy.CFG['log-format'])
    log_handle.setFormatter(log_format)
    
    swpy.LOG.addHandler(log_handle)
    swpy.LOG.setLevel(swpy.CFG['log-level'])
    
    

