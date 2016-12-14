from __future__ import absolute_import

## standard library
import os
from os import path
import sys
import logging

from swpy.swpy import  get_logger


SWPY_ROOT,_ = path.split(__path__[0])
SWPY_ROOT = SWPY_ROOT.replace('\\','/')
RESOURCE_DIR = SWPY_ROOT + '/res'
SCRIPT_DIR = SWPY_ROOT +'/scripts'
DOCUMENT_DIR = SWPY_ROOT + '/doc'
DATA_DIR = SWPY_ROOT +'/data'
TEMP_DIR = SWPY_ROOT +'/temp'

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


LOG.debug("# SWPY_ROOT = {}".format(SWPY_ROOT))



