## standard library
import logging
from utils.config import Config
from os import path
from utils.utils import make_path

## 3rd-party library


## included library
import sdo
import ace ,goes
#import cactus,seeds
#import dst
#import wilcox

from swpy import utils

CONFIG_FILE = 'swpy.ini'
SWPY_PATH = path.curdir
DATA_DIR  = 'data/'
META_DIR  = 'meta/' 
TEMP_DIR  = 'temp/'
LOG_DIR   = 'logs/'
LOG_LEVEL = logging.DEBUG
LOG = utils.get_logger(__name__)


def initialize(config=CONFIG_FILE):
    global LOG,SWPY_PATH,DATA_DIR,META_DIR,TEMP_DIR,LOG_DIR,LOG_LEVEL
    config = Config(CONFIG_FILE)
    SWPY_PATH = config.get_working_directory()

    ## Initialize for default
        
    DATA_DIR  = config.load('DATA_DIR', SWPY_PATH+'data'+path.sep)
    META_DIR  = config.load('META_DIR', SWPY_PATH+'meta'+path.sep) 
    TEMP_DIR  = config.load('TEMP_DIR', SWPY_PATH+'temp'+path.sep)
    LOG_DIR   = config.load('LOG_DIR',  SWPY_PATH+'logs'+path.sep)
    LOG_LEVEL = config.load('LOG_LEVEL',logging.DEBUG)


    DATA_DIR  = make_path(DATA_DIR)
    META_DIR  = make_path(META_DIR) 
    TEMP_DIR  = make_path(TEMP_DIR)
    LOG_DIR   = make_path(LOG_DIR)

    ## Initialize for library
    LOG = utils.get_logger(__name__)
    
    ## Initialize for sub-library
    ace.initialize(config)
    goes.initialize(config)
    sdo.initialize(config)
    
    config.write()


