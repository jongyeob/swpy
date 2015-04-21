## standard library
import logging
from utils.config import Config
from os import path
from utils.utils import make_path

## 3rd-party library


## included library
import sdo
import ace ,goes
import noaa
#import cactus,seeds
#import dst
#import wilcox

from swpy import utils


DATA_ROOT  = 'data/'
TEMP_DIR  = 'temp/'
LOG_DIR   = 'logs/'
LOG_LEVEL = logging.DEBUG


def initialize(config=''):
    if isinstance(config,str):
        config = Config(config)
    
    ## Initialize for default    
    config.load_ns('DATA_ROOT', globals())
    config.load_ns('TEMP_DIR', globals())
    config.load_ns('LOG_DIR',  globals())
    config.load_ns('LOG_LEVEL',globals())

    make_path(DATA_ROOT) 
    make_path(TEMP_DIR)
    make_path(LOG_DIR)

    ## Initialize for sub-library
    ace.initialize(config)
    goes.initialize(config)
    sdo.initialize(config)
    noaa.initialize(config)
    
    config.write()

