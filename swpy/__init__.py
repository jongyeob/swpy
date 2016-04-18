from __future__ import absolute_import

## standard library
import logging
import sys
import os
import os.path as path

from . import dst
from . import noaa
from . import sdo
from .utils import config

## included library
#import ace ,goes
#import cactus,seeds
#import wilcox

LOG = logging.getLogger(__name__)
LOG_LEVEL = 10
CONFIG_FILE = 'swpy.ini'

# __items = {}
# try:
#     __items = config.load(CONFIG_FILE)
# except IOError:
#     LOG.debug("Config file is not exist")
    
