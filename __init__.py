## standard library
import os
from os import path
import sys
import logging


## included library
import sdo
#import ace ,goes
import noaa
#import cactus,seeds
import dst
#import wilcox

from swpy import utils


LOG = logging.getLogger(__name__)
LOG_LEVEL = 10
CONFIG_FILE = 'swpy.ini'


def initialize(**kwargs):
    items = {}
    try:
        items = utils.config.load(CONFIG_FILE)
    except IOError:
        LOG.debug("Config file is not exist")
    
    utils.config.set(globals(),**items.pop(__name__,{}))
    
    sdo.initialize(**utils.config.get(items,sdo.__name__))
    noaa.initialize(**utils.config.get(items,noaa.__name__))
    dst.initialize(**utils.config.get(items,noaa.__name__))
    
