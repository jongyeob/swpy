## standard library
import logging
from utils.config import Config
from utils.utils import make_path


## 3rd-party library
LOG = logging.getLogger(__name__)

CONFIG_FILE = 'swpy.ini'
_cnf = Config(CONFIG_FILE,__name__)

## Configuration
SWPY_PATH = _cnf.get_working_directory()
DATA_DIR = _cnf.load('data_dir', make_path(SWPY_PATH+'/data/'))
META_DIR = _cnf.load('meta_dir',make_path(SWPY_PATH+'/meta/'))
TEMP_DIR = _cnf.load('temp_dir',make_path(SWPY_PATH+'/temp/'))
LOG_DIR = _cnf.load('log_dir',make_path(SWPY_PATH+'/logs/'))
LOG_LEVEL = _cnf.load('log_level',logging.WARN)

_cnf.write()

## Initialize
LOG.setLevel(int(LOG_LEVEL))

import sdo
sdo.initialize()







