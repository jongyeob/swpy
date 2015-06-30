import os
import logging
import tempfile
logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

from swpy.sdo import jsoc_hmi_fits
from swpy import utils
from swpy.utils import date_time as dt

jsoc_hmi_fits.DATA_DIR = tempfile.mkdtemp().replace('\\','/') + '/'

def test_download():
    end = dt.datetime.now()
    start = end - dt.timedelta(days=20)
    
    cadence = 7*86400 # seconds
    
    jsoc_hmi_fits.download(start,end,cadence)
    
    files = jsoc_hmi_fits.request(start,end,cadence)
    logging.debug('# files : %d'%(len(files)))
    

os.removedirs(jsoc_hmi_fits.DATA_DIR)