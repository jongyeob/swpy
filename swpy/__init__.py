from __future__ import absolute_import

## standard library
import os
from os import path
import sys
import logging


SWPY_ROOT,_ = path.split(__path__[0])
SWPY_ROOT = SWPY_ROOT.replace('\\','/')

## User configuration
LOG_FILE  = 'swpy.log'
LOG_FILE_MODE = 'w' # w, a if LOG_FILE exists
LOG_LEVEL = 10
LOG_FORMAT = "%(asctime)s %(name)s [%(levelname)s] %(message)s"

## Initialize 
_log_handle = logging.StreamHandler(sys.stderr)
if LOG_FILE:
    _log_handle = logging.FileHandler(LOG_FILE,LOG_FILE_MODE)
    
_log_format = logging.Formatter(LOG_FORMAT)
_log_handle.setFormatter(_log_format)

LOG = logging.getLogger('swpy')
LOG.addHandler(_log_handle)
LOG.setLevel(LOG_LEVEL)

## User configuration overwrite
try:
    from swpy_config import *
    LOG.deubug("# User config imported")

except:
    LOG.debug("# User config not imported")
    

LOG.debug("# SWPY_ROOT = {}".format(SWPY_ROOT))

def get_logger(name):
    if not name.startswith('swpy.'):
        name = 'swpy.' + name
    
    logger = logging.getLogger(name)
    logger.setLevel(0)
    
    return logger
