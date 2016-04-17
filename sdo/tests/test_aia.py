import os
import logging
import tempfile
logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

from swpy.sdo import aia
from swpy import utils
from swpy.utils import date_time as dt
    

aia.DATA_DIR = tempfile.mkdtemp().replace('\\','/') +'/'

def test_request():
    total = 0
    
    wavelength = '304'
    format = 'fits'
    
    filepath_format = aia.DATA_DIR + aia.DATA_FILE
    filepath_format = dt.replace(filepath_format,wavelength=wavelength,format=format,**aia.DATA_INFO)
    
    logging.debug("Test file format : %s"%(filepath_format))
    
    
    start = dt.parse('20150101_000000')
    end   = dt.parse('20150101_235959')
    cadence = 2*3600

    for _t in dt.series(start,end,hours=1):
        filepath = dt.replace(filepath_format,_t)
        utils.make_path(filepath)
        logging.debug("Create file : %s"%(filepath))
        if os.path.exists(filepath) == False:
            with open(filepath,"wb"): pass
        total += 1
    
    logging.debug("Total files : %d"%(total))
    
    ret = aia.request(start,wavelength,format)
    logging.debug("File(%s) : %s"%(str(start),str(ret)))
    
    ret = aia.request(start,wavelength,format,end_datetime=end)
    logging.debug("Number of Files : %d"%(len(ret)))
    
    ret = aia.request(start,wavelength,format,end_datetime=end,cadence=cadence)
    logging.debug("Number of Files (cadence:7200s) : %d"%(len(ret)))

def test_download_fits():
    start = dt.parse('20150601_000000')
    end   = dt.parse('20150601_020000')
    cadence = 2*3600
    
    wavelength = '304'
    aia.download_fits(start,wavelength,end_datetime=end,cadence=cadence,overwrite=True)
    
    files = aia.request(start, wavelength, 'fits', end, cadence)
    
    logging.debug("# downloaded files : %d"%(len(files)))
    