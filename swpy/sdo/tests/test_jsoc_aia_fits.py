import os
import logging
import tempfile
logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

from swpy.sdo import jsoc_aia_fits
from swpy import utils
from swpy.utils import date_time as dt

jsoc_aia_fits.DATA_DIR = tempfile.mkdtemp().replace('\\','/') + '/'

def test_download():
    end = dt.datetime.now()
    start = end - dt.timedelta(days=20)
    
    wave = '304'
    cadence = 7*86400 # seconds
    
    jsoc_aia_fits.download(start,wave,end,cadence)
    
    files = jsoc_aia_fits.request(start,wave,end,cadence)
    logging.debug('# files : %d'%(len(files)))