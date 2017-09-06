

## standard library
import os
import sys
from swpy.swpy import *
## Global setting

SWPY_ROOT,_ = os.path.split(__path__[0])
SWPY_ROOT = SWPY_ROOT.replace('\\','/')
RESOURCE_DIR = SWPY_ROOT + '/res'
SCRIPT_DIR = SWPY_ROOT +'/scripts'
DOCUMENT_DIR = SWPY_ROOT + '/doc'
DATA_DIR = SWPY_ROOT +'/data'
TEMP_DIR = SWPY_ROOT +'/temp'
CONFIG_FILE = SWPY_ROOT + '/swpy.ini'

## Default configuration
CFG = {
'log-level':10,
'log-format':"[%(levelname)s:%(name)s] %(message)s" }
CFG = get_config(CONFIG_FILE,CFG)

LOG = get_logger('swpy')
