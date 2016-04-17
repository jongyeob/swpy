'''
Created on 2015. 4. 24.

@author: jongyeob
'''

import os
import logging
import tempfile
logging.basicConfig(level=10,format=("%(asctime)s %(message)s"))

from swpy.sdo import hmi
from swpy import utils
from swpy.utils import date_time as dt
    

hmi.DATA_DIR = tempfile.mkdtemp().replace('\\','/') +'/'

def test_request():
    total = 0
    
    type = 'Ic_45s'
    format = 'fits'
    
    filepath_format = hmi.DATA_DIR + hmi.DATA_FILE
    filepath_format = dt.replace(filepath_format,type=type,format=format,**hmi.DATA_INFO)
    
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
    
    ret = hmi.request(start,type,format)
    logging.debug("File(%s) : %s"%(str(start),str(ret)))
    
    ret = hmi.request(start,type,format,end_datetime=end)
    logging.debug("Number of Files : %d"%(len(ret)))
    
    ret = hmi.request(start,type,format,end_datetime=end,cadence=cadence)
    logging.debug("Number of Files (cadence:7200s) : %d"%(len(ret)))

def test_download_fits():
    start = dt.parse('20150601_000000')
    end   = dt.parse('20150601_020000')
    cadence = 2*3600
    
    type = 'Ic_45s'
    hmi.download_fits(start,type,end_datetime=end,cadence=cadence,overwrite=True)
    
    files = hmi.request(start, type, 'fits', end, cadence)
    
    logging.debug("# downloaded files : %d"%(len(files)))
    
