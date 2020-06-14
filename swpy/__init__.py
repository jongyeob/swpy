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

from . import utils2

from .downloader import HttpDownloader, FtpDownloader
from .timepath import TimeFormat, Time
from .base import TimeUnit, DataUnit, PathUnit, PlotUnit
from .data import FitsData
from .client import ClientUnit
from .request import RequestUnit

## Default configuration
CFG = {
'log-level':10,
'log-format':"[%(levelname)s:%(name)s] %(message)s" }

LOG = None


def get_logger(name,log_format='',log_level=0):
    if not name:
        name = 'swpy'
    elif not name.startswith('swpy.'):
        name = 'swpy.' + name
    
    
    logger = logging.getLogger(name)
    
    log_handle = logging.StreamHandler(sys.stderr)
    log_format = logging.Formatter(log_format)
    log_handle.setFormatter(log_format)
    
    logger.addHandler(log_handle)
    logger.setLevel(log_level)
    
    return logger

def get_config(filepath,cfg):
    from . import utils
    
    num = utils.config.get_config(filepath,'swpy',cfg)
    return num

def init(log_level=0,config_file=''):
    global LOG
    
    if config_file:
        get_config(CONFIG_FILE,CFG)
        
    LOG = get_logger('swpy')
    
    utils2.testing.TEST_CACHE_FILE = os.path.join(TEMP_DIR, utils2.testing.TEST_CACHE_FILE)


    
init(CFG['log-level'],CFG['log-format'])
