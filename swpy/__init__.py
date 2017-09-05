

## standard library
import os
from os import path
import sys
import logging


SWPY_ROOT,_ = path.split(__path__[0])
SWPY_ROOT = SWPY_ROOT.replace('\\','/')
RESOURCE_DIR = SWPY_ROOT + '/res/'
SCRIPT_DIR = SWPY_ROOT +'/scripts/'
DOCUMENT_DIR = SWPY_ROOT + '/doc/'
DATA_DIR = SWPY_ROOT +'/data/'
TEMP_DIR = SWPY_ROOT +'/temp/'

## User configuration
LOG_LEVEL = 10
LOG_FORMAT = "%(asctime)s %(name)s [%(levelname)s] %(message)s"

## Initialize 
LOG = logging.getLogger('swpy')
LOG.setLevel(LOG_LEVEL)
LOG.addHandler(logging.NullHandler())


LOG.debug("# SWPY_ROOT = {}".format(SWPY_ROOT))


from .swpy import *

from . import base
from . import utils2
from . import solarpack