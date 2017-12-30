


## standard library
import os
import sys
import logging

## Global setting

SWPY_ROOT,_ = os.path.split(__path__[0])
SWPY_ROOT = SWPY_ROOT.replace('\\','/')
RESOURCE_DIR = SWPY_ROOT + '/res'
SCRIPT_DIR = SWPY_ROOT +'/scripts'
DOCUMENT_DIR = SWPY_ROOT + '/doc'
DATA_DIR = SWPY_ROOT +'/data'
TEMP_DIR = SWPY_ROOT +'/temp'
CONFIG_FILE = SWPY_ROOT + '/swpy.ini'

from utils2 import testing

from downloader import HttpDownloader, FtpDownloader
from timepath import TimeFormat, Time


def get_logger(name):
    if not name:
        name = 'swpy'
    elif not name.startswith('swpy.'):
        name = 'swpy.' + name
    
    logger = logging.getLogger(name)
    logger.setLevel(0)
    
    return logger

def get_config(filepath,cfg):
    import utils
    
    num = utils.config.get_config(filepath,'swpy',cfg)
    return num

def init(log_level=20,config_file=''):
    if config_file:
        get_config(config_file,CFG)

    log_handle = logging.StreamHandler(sys.stderr)
    log_format = logging.Formatter(CFG['log-format'])
    log_handle.setFormatter(log_format)
    
    LOG.addHandler(log_handle)
    LOG.setLevel(CFG['log-level'])
    
## Default configuration
CFG = {
'log-level':10,
'log-format':"[%(levelname)s:%(name)s] %(message)s" }
CFG = get_config(CONFIG_FILE,CFG)
LOG = get_logger('swpy')

testing.TEST_CACHE_FILE = os.path.join(TEMP_DIR, testing.TEST_CACHE_FILE)